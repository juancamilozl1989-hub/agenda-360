import { useCallback, useEffect, useMemo, useState } from "react";

import {
  Alert,
  Box,
  CircularProgress,
  IconButton,
  MenuItem,
  TextField,
} from "@mui/material";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/tables/DataTable";
import AppSnackbar from "../../components/common/AppSnackbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import HorarioFormModal from "../../components/modals/HorarioFormModal";

import {
  actualizarHorario,
  crearHorario,
  eliminarHorario,
  listarHorarios,
} from "../../api/horariosService";
import { listarBarberos } from "../../api/barberosService";
import { mensajeError } from "../../api/errores";
import { DIAS_SEMANA } from "../../api/tipos";
import type { Barbero, Horario, HorarioForm } from "../../api/tipos";

// ==========================================================
// Horarios de atención
// ==========================================================
// Aquí el administrador define en qué días y horas atiende cada
// barbero. La agenda y el bot de WhatsApp solo ofrecen horas
// dentro de estos bloques.

export default function HorariosPage() {
  const [horarios, setHorarios] = useState<Horario[]>([]);
  const [barberos, setBarberos] = useState<Barbero[]>([]);
  const [filtroBarbero, setFiltroBarbero] = useState<number>(0);
  const [cargando, setCargando] = useState(true);

  const [openModal, setOpenModal] = useState(false);
  const [horarioEditar, setHorarioEditar] = useState<HorarioForm | null>(null);
  const [horarioEliminar, setHorarioEliminar] = useState<Horario | null>(null);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });

  const avisar = (
    message: string,
    severity: "success" | "error" | "warning" = "success"
  ) => setSnackbar({ open: true, message, severity });

  const cargarDatos = useCallback(async () => {
    try {
      const [h, b] = await Promise.all([listarHorarios(), listarBarberos()]);
      setHorarios(h);
      setBarberos(b);
    } catch (error) {
      avisar(mensajeError(error, "No se pudieron cargar los horarios."), "error");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  // Orden: barbero, día de la semana (lunes a domingo) y hora de inicio
  const filas = useMemo(
    () =>
      horarios
        .filter((h) => !filtroBarbero || h.barber.id === filtroBarbero)
        .sort(
          (a, b) =>
            a.barber.nombre.localeCompare(b.barber.nombre) ||
            DIAS_SEMANA.indexOf(a.dia_semana) - DIAS_SEMANA.indexOf(b.dia_semana) ||
            a.hora_inicio.localeCompare(b.hora_inicio)
        ),
    [horarios, filtroBarbero]
  );

  // Barberos activos que todavía no tienen ningún horario: no pueden recibir citas
  const sinHorario = barberos.filter(
    (b) => b.estado === "Activo" && !horarios.some((h) => h.barber.id === b.id)
  );

  const handleGuardar = async (lista: HorarioForm[]): Promise<boolean> => {
    // Al editar llega un solo bloque; al crear, uno por cada día marcado
    if (lista.length === 1 && lista[0].id !== 0) {
      try {
        await actualizarHorario(lista[0]);
        avisar("Horario actualizado correctamente.");
        setHorarioEditar(null);
        await cargarDatos();
        return true;
      } catch (error) {
        avisar(mensajeError(error, "No se pudo actualizar el horario."), "error");
        return false;
      }
    }

    const errores: string[] = [];
    let creados = 0;

    for (const horario of lista) {
      try {
        await crearHorario(horario);
        creados += 1;
      } catch (error) {
        errores.push(`${horario.dia_semana}: ${mensajeError(error, "error")}`);
      }
    }

    await cargarDatos();

    if (errores.length === 0) {
      avisar(
        creados === 1
          ? "Horario creado correctamente."
          : `Se crearon ${creados} horarios.`
      );
      return true;
    }

    avisar(
      `Se crearon ${creados} de ${lista.length}. ${errores.join(" ")}`,
      creados > 0 ? "warning" : "error"
    );
    return false;
  };

  const handleEliminar = async () => {
    if (!horarioEliminar) return;

    try {
      await eliminarHorario(horarioEliminar.id);
      avisar("Horario eliminado correctamente.");
      await cargarDatos();
    } catch (error) {
      avisar(mensajeError(error, "No se pudo eliminar el horario."), "error");
    } finally {
      setHorarioEliminar(null);
    }
  };

  const columns = [
    {
      field: "barber",
      headerName: "Barbero",
      render: (value: { nombre: string }) => value.nombre,
    },
    { field: "dia_semana", headerName: "Día" },
    {
      field: "hora_inicio",
      headerName: "Desde",
      render: (value: string) => value.slice(0, 5),
    },
    {
      field: "hora_fin",
      headerName: "Hasta",
      render: (value: string) => value.slice(0, 5),
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Horarios"
        subtitle="Días y horas en que atiende cada barbero. La agenda solo ofrece turnos dentro de estos bloques."
        buttonText="Nuevo horario"
        onClick={() => {
          setHorarioEditar(null);
          setOpenModal(true);
        }}
      />

      {!cargando && sinHorario.length > 0 && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {sinHorario.map((b) => b.nombre).join(", ")}{" "}
          {sinHorario.length === 1 ? "no tiene" : "no tienen"} horario
          registrado y no podrá{sinHorario.length === 1 ? "" : "n"} recibir
          citas hasta que se le asigne uno.
        </Alert>
      )}

      <TextField
        select
        size="small"
        label="Barbero"
        value={filtroBarbero}
        onChange={(e) => setFiltroBarbero(Number(e.target.value))}
        sx={{ minWidth: 240, mb: 3 }}
      >
        <MenuItem value={0}>Todos los barberos</MenuItem>
        {barberos.map((b) => (
          <MenuItem key={b.id} value={b.id}>
            {b.nombre}
          </MenuItem>
        ))}
      </TextField>

      {cargando ? (
        <Box display="flex" justifyContent="center" py={6}>
          <CircularProgress sx={{ color: "#D4AF37" }} />
        </Box>
      ) : (
        <DataTable
          columns={columns}
          rows={filas}
          renderActions={(row: Horario) => (
            <>
              <IconButton
                color="primary"
                onClick={() => {
                  setHorarioEditar({
                    id: row.id,
                    dia_semana: row.dia_semana,
                    hora_inicio: row.hora_inicio.slice(0, 5),
                    hora_fin: row.hora_fin.slice(0, 5),
                    barber_id: row.barber.id,
                  });
                  setOpenModal(true);
                }}
              >
                <EditIcon />
              </IconButton>

              <IconButton color="error" onClick={() => setHorarioEliminar(row)}>
                <DeleteIcon />
              </IconButton>
            </>
          )}
        />
      )}

      <HorarioFormModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setHorarioEditar(null);
        }}
        onSave={handleGuardar}
        horarioEditar={horarioEditar}
        barberos={barberos}
      />

      <ConfirmDialog
        open={horarioEliminar !== null}
        title="Eliminar horario"
        message={`¿Eliminar el horario del ${
          horarioEliminar?.dia_semana.toLowerCase() ?? ""
        } de ${horarioEliminar?.barber.nombre ?? ""}?`}
        onConfirm={handleEliminar}
        onCancel={() => setHorarioEliminar(null)}
      />

      <AppSnackbar
        open={snackbar.open}
        message={snackbar.message}
        severity={snackbar.severity}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      />
    </Box>
  );
}
