import { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";

import { consultarDisponibilidad } from "../../api/disponibilidadService";
import { mensajeError } from "../../api/errores";
import type {
  Barbero,
  CitaForm,
  Cliente,
  HoraDisponible,
  Servicio,
} from "../../api/tipos";

interface CitaFormModalProps {
  open: boolean;
  onClose: () => void;
  // Devuelve true si la API aceptó el cambio; solo entonces se cierra el modal.
  onSave: (cita: CitaForm) => Promise<boolean>;
  citaEditar?: CitaForm | null;
  clientes: Cliente[];
  barberos: Barbero[];
  servicios: Servicio[];
}

// Valor especial del selector de barbero: el sistema asigna
// el primer barbero libre a la hora elegida.
const CUALQUIERA = "cualquiera";

// Fecha local de hoy en formato AAAA-MM-DD (lo que espera el input date y la API).
const hoy = () => {
  const d = new Date();
  const mes = String(d.getMonth() + 1).padStart(2, "0");
  const dia = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${mes}-${dia}`;
};

const vacio = (): CitaForm => ({
  id: 0,
  fecha: hoy(),
  hora: "",
  estado: "Pendiente",
  client_id: 0,
  barber_id: 0,
  service_id: 0,
});

export default function CitaFormModal({
  open,
  onClose,
  onSave,
  citaEditar,
  clientes,
  barberos,
  servicios,
}: CitaFormModalProps) {
  const [formData, setFormData] = useState<CitaForm>(vacio());
  // "" (sin elegir), "cualquiera" o el id del barbero como texto
  const [barbero, setBarbero] = useState("");
  const [horas, setHoras] = useState<HoraDisponible[]>([]);
  const [cargandoHoras, setCargandoHoras] = useState(false);
  const [avisoHoras, setAvisoHoras] = useState("");
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    const inicial = citaEditar ?? vacio();
    setFormData(inicial);
    setBarbero(inicial.barber_id ? String(inicial.barber_id) : "");
    setError("");
  }, [citaEditar, open]);

  // ==========================================================
  // Horas disponibles
  // ==========================================================
  // Las horas no se escriben a mano: se piden a la API de
  // disponibilidad, que aplica el horario del barbero, la duración
  // del servicio y las citas ya registradas. Es la misma consulta
  // que usará el bot de WhatsApp.
  useEffect(() => {
    if (!open || !formData.service_id || !formData.fecha || !barbero) {
      setHoras([]);
      setAvisoHoras("");
      return;
    }

    let vigente = true;
    setCargandoHoras(true);
    setAvisoHoras("");

    consultarDisponibilidad(
      formData.fecha,
      formData.service_id,
      barbero === CUALQUIERA ? undefined : Number(barbero)
    )
      .then((d) => {
        if (!vigente) return;
        setHoras(d.disponibles);
        if (d.disponibles.length === 0) {
          setAvisoHoras(
            `No hay horas libres el ${d.dia_semana.toLowerCase()} ${d.fecha}. ` +
              "Prueba otra fecha u otro barbero, o revisa sus horarios."
          );
        }
      })
      .catch((e) => {
        if (!vigente) return;
        setHoras([]);
        setAvisoHoras(mensajeError(e, "No se pudo consultar la disponibilidad."));
      })
      .finally(() => vigente && setCargandoHoras(false));

    return () => {
      vigente = false;
    };
  }, [open, formData.service_id, formData.fecha, barbero]);

  // Al editar, la hora actual de la cita no aparece como libre
  // (la ocupa ella misma), así que se agrega a las opciones si la
  // fecha y el barbero no han cambiado.
  const horaActual = useMemo(() => {
    if (
      !citaEditar ||
      formData.fecha !== citaEditar.fecha ||
      barbero !== String(citaEditar.barber_id)
    ) {
      return null;
    }
    return citaEditar.hora.slice(0, 5);
  }, [citaEditar, formData.fecha, barbero]);

  const opcionesHora = useMemo(() => {
    const opciones = horas.map((h) => ({
      valor: h.hora.slice(0, 5),
      etiqueta:
        barbero === CUALQUIERA
          ? `${h.hora.slice(0, 5)} · ${h.barberos.map((b) => b.nombre).join(", ")}`
          : h.hora.slice(0, 5),
    }));

    if (horaActual && !opciones.some((o) => o.valor === horaActual)) {
      opciones.push({ valor: horaActual, etiqueta: `${horaActual} (hora actual)` });
      opciones.sort((a, b) => a.valor.localeCompare(b.valor));
    }

    return opciones;
  }, [horas, horaActual, barbero]);

  // Si la hora elegida deja de estar disponible (cambió la fecha,
  // el servicio o el barbero), se limpia para obligar a escoger otra.
  useEffect(() => {
    if (
      formData.hora &&
      !cargandoHoras &&
      !opcionesHora.some((o) => o.valor === formData.hora.slice(0, 5))
    ) {
      setFormData((f) => ({ ...f, hora: "" }));
    }
  }, [opcionesHora, cargandoHoras, formData.hora]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]:
        name === "client_id" || name === "service_id"
          ? Number(value)
          : value,
    });
  };

  const handleSave = async () => {
    if (
      !formData.client_id ||
      !formData.service_id ||
      !barbero ||
      !formData.fecha ||
      !formData.hora
    ) {
      setError("Todos los campos son obligatorios.");
      return;
    }

    // "Cualquier barbero": se asigna el primero que esté libre a esa hora
    let barberId = Number(barbero);
    if (barbero === CUALQUIERA) {
      const libre = horas.find((h) => h.hora.startsWith(formData.hora));
      if (!libre || libre.barberos.length === 0) {
        setError("Esa hora ya no está disponible. Elige otra.");
        return;
      }
      barberId = libre.barberos[0].id;
    }

    setError("");
    setGuardando(true);
    const guardado = await onSave({ ...formData, barber_id: barberId });
    setGuardando(false);

    if (guardado) onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>
        {citaEditar ? "Editar Cita" : "Nueva Cita"}
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3} mt={1}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            select
            label="Cliente"
            name="client_id"
            value={formData.client_id || ""}
            onChange={handleChange}
            fullWidth
          >
            {clientes
              .filter((c) => c.estado === "Activo" || c.id === formData.client_id)
              .map((c) => (
                <MenuItem key={c.id} value={c.id}>
                  {c.nombre}
                </MenuItem>
              ))}
          </TextField>

          <TextField
            select
            label="Servicio"
            name="service_id"
            value={formData.service_id || ""}
            onChange={handleChange}
            fullWidth
            helperText="Cualquier barbero activo puede atender cualquier servicio."
          >
            {servicios
              .filter((s) => s.estado === "Activo" || s.id === formData.service_id)
              .map((s) => (
                <MenuItem key={s.id} value={s.id}>
                  {s.nombre} · {s.duracion} min
                </MenuItem>
              ))}
          </TextField>

          <TextField
            select
            label="Barbero"
            value={barbero}
            onChange={(e) => setBarbero(e.target.value)}
            fullWidth
          >
            {!citaEditar && (
              <MenuItem value={CUALQUIERA}>
                Cualquier barbero disponible
              </MenuItem>
            )}
            {barberos
              .filter((b) => b.estado === "Activo" || String(b.id) === barbero)
              .map((b) => (
                <MenuItem key={b.id} value={String(b.id)}>
                  {b.nombre}
                </MenuItem>
              ))}
          </TextField>

          <Stack direction="row" spacing={2}>
            <TextField
              label="Fecha"
              name="fecha"
              type="date"
              value={formData.fecha}
              onChange={handleChange}
              fullWidth
              slotProps={{
                inputLabel: { shrink: true },
                htmlInput: citaEditar ? {} : { min: hoy() },
              }}
            />

            <TextField
              select
              label="Hora"
              name="hora"
              value={opcionesHora.some((o) => o.valor === formData.hora.slice(0, 5))
                ? formData.hora.slice(0, 5)
                : ""}
              onChange={handleChange}
              fullWidth
              disabled={cargandoHoras || opcionesHora.length === 0}
              slotProps={{
                input: {
                  endAdornment: cargandoHoras ? (
                    <CircularProgress size={18} sx={{ mr: 3 }} />
                  ) : undefined,
                },
              }}
            >
              {opcionesHora.map((o) => (
                <MenuItem key={o.valor} value={o.valor}>
                  {o.etiqueta}
                </MenuItem>
              ))}
            </TextField>
          </Stack>

          {(!formData.service_id || !barbero) && (
            <Alert severity="info">
              Elige el servicio y el barbero para ver las horas disponibles.
            </Alert>
          )}

          {avisoHoras && opcionesHora.length === 0 && (
            <Alert severity="warning">{avisoHoras}</Alert>
          )}

          {citaEditar && (
            <TextField
              select
              label="Estado"
              name="estado"
              value={formData.estado}
              onChange={handleChange}
              fullWidth
            >
              <MenuItem value="Pendiente">Pendiente</MenuItem>
              <MenuItem value="Confirmada">Confirmada</MenuItem>
              <MenuItem value="Completada">Completada</MenuItem>
              <MenuItem value="Cancelada">Cancelada</MenuItem>
            </TextField>
          )}
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose}>Cancelar</Button>

        <Button
          variant="contained"
          onClick={handleSave}
          disabled={guardando}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            "&:hover": { bgcolor: "#C49A1D" },
          }}
        >
          {citaEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
