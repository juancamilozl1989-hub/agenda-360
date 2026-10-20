import { useCallback, useEffect, useMemo, useState } from "react";

import {
  Avatar,
  Box,
  Chip,
  CircularProgress,
  IconButton,
  InputAdornment,
  TextField,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/tables/DataTable";
import AppSnackbar from "../../components/common/AppSnackbar";
import ConfirmDialog from "../../components/common/ConfirmDialog";
import BarberoFormModal from "../../components/modals/BarberoFormModal";

import {
  actualizarBarbero,
  crearBarbero,
  eliminarBarbero,
  listarBarberos,
} from "../../api/barberosService";
import { obtenerBarberiaPrincipal } from "../../api/barberiasService";
import { mensajeError } from "../../api/errores";
import type { Barbero, BarberoForm } from "../../api/tipos";

export default function BarberosPage() {
  const [openModal, setOpenModal] = useState(false);
  const [barberoEditar, setBarberoEditar] =
    useState<BarberoForm | null>(null);
  const [barberoEliminar, setBarberoEliminar] =
    useState<Barbero | null>(null);
  const [busqueda, setBusqueda] = useState("");
  const [barberos, setBarberos] = useState<Barbero[]>([]);
  const [cargando, setCargando] = useState(true);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as "success" | "error" | "warning" | "info",
  });

  const avisar = (
    message: string,
    severity: "success" | "error" = "success"
  ) => setSnackbar({ open: true, message, severity });

  const cargarBarberos = useCallback(async () => {
    try {
      setBarberos(await listarBarberos());
    } catch (error) {
      avisar(mensajeError(error, "No se pudieron cargar los barberos."), "error");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarBarberos();
  }, [cargarBarberos]);

  const barberosFiltrados = useMemo(() => {
    const texto = busqueda.toLowerCase();

    return barberos.filter(
      (b) =>
        b.nombre.toLowerCase().includes(texto) ||
        b.especialidad.toLowerCase().includes(texto) ||
        b.telefono.includes(texto)
    );
  }, [barberos, busqueda]);

  const handleGuardarBarbero = async (
    form: BarberoForm
  ): Promise<boolean> => {
    try {
      const barberia = await obtenerBarberiaPrincipal();

      if (form.id === 0) {
        await crearBarbero(form, barberia.id);
        avisar("Barbero creado correctamente.");
      } else {
        await actualizarBarbero(form, barberia.id);
        avisar("Barbero actualizado correctamente.");
      }

      setBarberoEditar(null);
      await cargarBarberos();
      return true;
    } catch (error) {
      avisar(mensajeError(error, "No se pudo guardar el barbero."), "error");
      return false;
    }
  };

  const handleEliminarBarbero = async () => {
    if (!barberoEliminar) return;

    try {
      await eliminarBarbero(barberoEliminar.id);
      avisar("Barbero eliminado correctamente.");
      await cargarBarberos();
    } catch (error) {
      avisar(mensajeError(error, "No se pudo eliminar el barbero."), "error");
    } finally {
      setBarberoEliminar(null);
    }
  };

  const columns = [
    {
      field: "avatar",
      headerName: "",
      render: (_: unknown, row: Barbero) => (
        <Avatar
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
          }}
        >
          {row.nombre.charAt(0)}
        </Avatar>
      ),
    },
    { field: "nombre", headerName: "Nombre" },
    { field: "especialidad", headerName: "Especialidad" },
    { field: "telefono", headerName: "Teléfono" },
    {
      field: "estado",
      headerName: "Estado",
      render: (value: string) => (
        <Chip
          label={value}
          color={value === "Activo" ? "success" : "default"}
          size="small"
        />
      ),
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Barberos"
        subtitle="Administra los barberos registrados."
        buttonText="Nuevo Barbero"
        onClick={() => {
          setBarberoEditar(null);
          setOpenModal(true);
        }}
      />

      <TextField
        fullWidth
        placeholder="Buscar barbero..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        sx={{ mb: 3 }}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          },
        }}
      />

      {cargando ? (
        <Box display="flex" justifyContent="center" py={6}>
          <CircularProgress sx={{ color: "#D4AF37" }} />
        </Box>
      ) : (
        <DataTable
          columns={columns}
          rows={barberosFiltrados}
          renderActions={(row) => (
            <>
              <IconButton
                color="primary"
                onClick={() => {
                  setBarberoEditar({
                    id: row.id,
                    nombre: row.nombre,
                    especialidad: row.especialidad,
                    telefono: row.telefono,
                    estado: row.estado,
                  });
                  setOpenModal(true);
                }}
              >
                <EditIcon />
              </IconButton>

              <IconButton
                color="error"
                onClick={() => setBarberoEliminar(row)}
              >
                <DeleteIcon />
              </IconButton>
            </>
          )}
        />
      )}

      <BarberoFormModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setBarberoEditar(null);
        }}
        onSave={handleGuardarBarbero}
        barberoEditar={barberoEditar}
      />

      <ConfirmDialog
        open={barberoEliminar !== null}
        title="Eliminar Barbero"
        message={`¿Está seguro de eliminar a ${
          barberoEliminar?.nombre ?? ""
        }?`}
        onConfirm={handleEliminarBarbero}
        onCancel={() => setBarberoEliminar(null)}
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
