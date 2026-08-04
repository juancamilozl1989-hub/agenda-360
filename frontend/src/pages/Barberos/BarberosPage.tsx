import { useMemo, useState } from "react";

import {
  Avatar,
  Box,
  Chip,
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
import type { Barbero } from "../../components/modals/BarberoFormModal";

export default function BarberosPage() {
  const [openModal, setOpenModal] = useState(false);

  const [barberoEditar, setBarberoEditar] =
    useState<Barbero | null>(null);

  const [barberoEliminar, setBarberoEliminar] =
    useState<Barbero | null>(null);

  const [busqueda, setBusqueda] = useState("");

  const [barberos, setBarberos] = useState<Barbero[]>([
    {
      id: 1,
      nombre: "Andrés López",
      especialidad: "Fade",
      telefono: "3001234567",
      estado: "Activo",
    },
    {
      id: 2,
      nombre: "Sebastián Gómez",
      especialidad: "Barba",
      telefono: "3014567890",
      estado: "Activo",
    },
    {
      id: 3,
      nombre: "Juan Rojas",
      especialidad: "Color",
      telefono: "3209876543",
      estado: "Inactivo",
    },
  ]);

  const [snackbar, setSnackbar] = useState({
    open: false,
    message: "",
    severity: "success" as
      | "success"
      | "error"
      | "warning"
      | "info",
  });

  const barberosFiltrados = useMemo(() => {
    const texto = busqueda.toLowerCase();

    return barberos.filter(
      (b) =>
        b.nombre.toLowerCase().includes(texto) ||
        b.especialidad.toLowerCase().includes(texto) ||
        b.telefono.includes(texto)
    );
  }, [barberos, busqueda]);

  const handleGuardarBarbero = (
    barbero: Barbero
  ) => {
    const existe = barberos.some(
      (b) => b.id === barbero.id
    );

    if (existe) {
      setBarberos(
        barberos.map((b) =>
          b.id === barbero.id ? barbero : b
        )
      );

      setSnackbar({
        open: true,
        message:
          "Barbero actualizado correctamente.",
        severity: "success",
      });
    } else {
      setBarberos([...barberos, barbero]);

      setSnackbar({
        open: true,
        message:
          "Barbero creado correctamente.",
        severity: "success",
      });
    }

    setBarberoEditar(null);
  };

  const handleEliminarBarbero = () => {
    if (!barberoEliminar) return;

    setBarberos(
      barberos.filter(
        (b) => b.id !== barberoEliminar.id
      )
    );

    setSnackbar({
      open: true,
      message:
        "Barbero eliminado correctamente.",
      severity: "success",
    });

    setBarberoEliminar(null);
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
    {
      field: "nombre",
      headerName: "Nombre",
    },
    {
      field: "especialidad",
      headerName: "Especialidad",
    },
    {
      field: "telefono",
      headerName: "Teléfono",
    },
    {
      field: "estado",
      headerName: "Estado",
      render: (value: string) => (
        <Chip
          label={value}
          color={
            value === "Activo"
              ? "success"
              : "default"
          }
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
        onChange={(e) =>
          setBusqueda(e.target.value)
        }
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

      <DataTable
        columns={columns}
        rows={barberosFiltrados}
        renderActions={(row) => (
          <>
            <IconButton
              color="primary"
              onClick={() => {
                setBarberoEditar(row);
                setOpenModal(true);
              }}
            >
              <EditIcon />
            </IconButton>

            <IconButton
              color="error"
              onClick={() =>
                setBarberoEliminar(row)
              }
            >
              <DeleteIcon />
            </IconButton>
          </>
        )}
      />

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
        onCancel={() =>
          setBarberoEliminar(null)
        }
      />

      <AppSnackbar
        open={snackbar.open}
        message={snackbar.message}
        severity={snackbar.severity}
        onClose={() =>
          setSnackbar({
            ...snackbar,
            open: false,
          })
        }
      />
    </Box>
  );
}