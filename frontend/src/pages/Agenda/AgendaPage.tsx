import { useCallback, useEffect, useMemo, useState } from "react";

import {
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";

import TimeLine from "../../components/agenda/TimeLine";
import CitaFormModal from "../../components/modals/CitaFormModal";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import AppSnackbar from "../../components/common/AppSnackbar";

import {
  actualizarCita,
  crearCita,
  eliminarCita,
  listarCitas,
} from "../../api/citasService";
import { listarClientes } from "../../api/clientesService";
import { listarBarberos } from "../../api/barberosService";
import { listarServicios } from "../../api/serviciosService";
import { mensajeError } from "../../api/errores";
import type {
  Barbero,
  Cita,
  CitaForm,
  Cliente,
  Servicio,
} from "../../api/tipos";
import {
  hoyTexto,
  inicioSemana,
  mismoMes,
  sumarDias,
} from "../../utils/fechas";

export default function AgendaPage() {
  const [pestana, setPestana] = useState(0);
  const [citas, setCitas] = useState<Cita[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [barberos, setBarberos] = useState<Barbero[]>([]);
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [cargando, setCargando] = useState(true);

  const [openModal, setOpenModal] = useState(false);
  const [citaEditar, setCitaEditar] = useState<CitaForm | null>(null);
  const [citaEliminar, setCitaEliminar] = useState<Cita | null>(null);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });

  const avisar = (
    message: string,
    severity: "success" | "error" = "success"
  ) => setSnackbar({ open: true, message, severity });

  const cargarDatos = useCallback(async () => {
    try {
      const [c, cl, b, s] = await Promise.all([
        listarCitas(),
        listarClientes(),
        listarBarberos(),
        listarServicios(),
      ]);
      setCitas(c);
      setClientes(cl);
      setBarberos(b);
      setServicios(s);
    } catch (error) {
      avisar(mensajeError(error, "No se pudo cargar la agenda."), "error");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  // Filtra por pestaña (Hoy / Semana / Mes) y ordena cronológicamente
  const citasVisibles = useMemo(() => {
    const hoy = hoyTexto();
    const lunes = inicioSemana(hoy);
    const domingo = sumarDias(lunes, 6);

    return citas
      .filter((c) => {
        if (pestana === 0) return c.fecha === hoy;
        if (pestana === 1) return c.fecha >= lunes && c.fecha <= domingo;
        return mismoMes(c.fecha, hoy);
      })
      .sort((a, b) =>
        `${a.fecha} ${a.hora}`.localeCompare(`${b.fecha} ${b.hora}`)
      );
  }, [citas, pestana]);

  const handleGuardarCita = async (
    form: CitaForm
  ): Promise<boolean> => {
    try {
      if (form.id === 0) {
        await crearCita(form);
        avisar("Cita creada correctamente.");
      } else {
        await actualizarCita(form);
        avisar("Cita actualizada correctamente.");
      }

      setCitaEditar(null);
      await cargarDatos();
      return true;
    } catch (error) {
      // Aquí llegan las reglas de negocio del backend
      // (fecha u hora pasada, fuera del horario del barbero, cruce con otra cita...)
      avisar(mensajeError(error, "No se pudo guardar la cita."), "error");
      return false;
    }
  };

  const handleEliminarCita = async () => {
    if (!citaEliminar) return;

    try {
      await eliminarCita(citaEliminar.id);
      avisar("Cita eliminada correctamente.");
      await cargarDatos();
    } catch (error) {
      avisar(mensajeError(error, "No se pudo eliminar la cita."), "error");
    } finally {
      setCitaEliminar(null);
    }
  };

  return (
    <Box>
      {/* Encabezado */}
      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 4 }}
      >
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Agenda de Citas
          </Typography>

          <Typography color="text.secondary">
            Administra todas las citas de tu barbería.
          </Typography>
        </Box>

        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setCitaEditar(null);
            setOpenModal(true);
          }}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            borderRadius: 3,
            px: 3,

            "&:hover": {
              bgcolor: "#E5C04A",
            },
          }}
        >
          Nueva cita
        </Button>
      </Stack>

      {/* Pestañas */}
      <Tabs
        value={pestana}
        onChange={(_, valor) => setPestana(valor)}
        sx={{
          mb: 3,

          "& .MuiTabs-indicator": {
            backgroundColor: "#D4AF37",
            height: 3,
            borderRadius: 2,
          },

          "& .MuiTab-root": {
            color: "#999",
            textTransform: "none",
            fontWeight: 600,
            fontSize: 15,
          },

          "& .Mui-selected": {
            color: "#D4AF37 !important",
          },
        }}
      >
        <Tab label="Hoy" />
        <Tab label="Semana" />
        <Tab label="Mes" />
      </Tabs>

      {/* Contenedor de la Agenda */}
      <Paper
        elevation={0}
        sx={{
          borderRadius: 4,
          bgcolor: "#1E1E1E",
          border: "1px solid rgba(255,255,255,.08)",
          p: 3,
        }}
      >
        {cargando ? (
          <Box display="flex" justifyContent="center" py={6}>
            <CircularProgress sx={{ color: "#D4AF37" }} />
          </Box>
        ) : (
          <TimeLine
            citas={citasVisibles}
            mostrarFecha={pestana !== 0}
            onEdit={(cita) => {
              setCitaEditar({
                id: cita.id,
                fecha: cita.fecha,
                hora: cita.hora.slice(0, 5),
                estado: cita.estado,
                client_id: cita.client.id,
                barber_id: cita.barber.id,
                service_id: cita.service.id,
              });
              setOpenModal(true);
            }}
            onDelete={setCitaEliminar}
          />
        )}
      </Paper>

      <CitaFormModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setCitaEditar(null);
        }}
        onSave={handleGuardarCita}
        citaEditar={citaEditar}
        clientes={clientes}
        barberos={barberos}
        servicios={servicios}
      />

      <ConfirmDialog
        open={citaEliminar !== null}
        title="Eliminar Cita"
        message={`¿Está seguro de eliminar la cita de ${
          citaEliminar?.client.nombre ?? ""
        }?`}
        onConfirm={handleEliminarCita}
        onCancel={() => setCitaEliminar(null)}
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
