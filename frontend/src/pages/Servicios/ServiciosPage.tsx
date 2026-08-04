import { useMemo, useState } from "react";

import {
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

import ServicioFormModal from "../../components/modals/ServicioFormModal";
import type { Servicio } from "../../components/modals/ServicioFormModal";

export default function ServiciosPage() {
  const [openModal, setOpenModal] = useState(false);

  const [servicioEditar, setServicioEditar] =
    useState<Servicio | null>(null);

  const [servicioEliminar, setServicioEliminar] =
    useState<Servicio | null>(null);

  const [busqueda, setBusqueda] = useState("");

  const [servicios, setServicios] = useState<Servicio[]>([
    {
      id: 1,
      nombre: "Corte Clásico",
      categoria: "Corte",
      duracion: 30,
      precio: 25000,
      estado: "Activo",
    },
    {
      id: 2,
      nombre: "Fade",
      categoria: "Corte",
      duracion: 45,
      precio: 35000,
      estado: "Activo",
    },
    {
      id: 3,
      nombre: "Barba Premium",
      categoria: "Barba",
      duracion: 20,
      precio: 18000,
      estado: "Activo",
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

  const serviciosFiltrados = useMemo(() => {
    const texto = busqueda.toLowerCase();

    return servicios.filter(
      (s) =>
        s.nombre.toLowerCase().includes(texto) ||
        s.categoria.toLowerCase().includes(texto)
    );
  }, [servicios, busqueda]);

  const handleGuardarServicio = (
    servicio: Servicio
  ) => {
    const existe = servicios.some(
      (s) => s.id === servicio.id
    );

    if (existe) {
      setServicios(
        servicios.map((s) =>
          s.id === servicio.id ? servicio : s
        )
      );

      setSnackbar({
        open: true,
        message:
          "Servicio actualizado correctamente.",
        severity: "success",
      });
    } else {
      setServicios([...servicios, servicio]);

      setSnackbar({
        open: true,
        message:
          "Servicio creado correctamente.",
        severity: "success",
      });
    }

    setServicioEditar(null);
  };

  const handleEliminarServicio = () => {
    if (!servicioEliminar) return;

    setServicios(
      servicios.filter(
        (s) => s.id !== servicioEliminar.id
      )
    );

    setSnackbar({
      open: true,
      message:
        "Servicio eliminado correctamente.",
      severity: "success",
    });

    setServicioEliminar(null);
  };

  const columns = [
    {
      field: "nombre",
      headerName: "Servicio",
    },
    {
      field: "categoria",
      headerName: "Categoría",
    },
    {
      field: "duracion",
      headerName: "Duración",
      render: (value: number) => `${value} min`,
    },
    {
      field: "precio",
      headerName: "Precio",
      render: (value: number) =>
        value.toLocaleString("es-CO", {
          style: "currency",
          currency: "COP",
        }),
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
        title="Servicios"
        subtitle="Administra los servicios de la barbería."
        buttonText="Nuevo Servicio"
        onClick={() => {
          setServicioEditar(null);
          setOpenModal(true);
        }}
      />

      <TextField
        fullWidth
        placeholder="Buscar servicio..."
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
        rows={serviciosFiltrados}
        renderActions={(row) => (
          <>
            <IconButton
              color="primary"
              onClick={() => {
                setServicioEditar(row);
                setOpenModal(true);
              }}
            >
              <EditIcon />
            </IconButton>

            <IconButton
              color="error"
              onClick={() =>
                setServicioEliminar(row)
              }
            >
              <DeleteIcon />
            </IconButton>
          </>
        )}
      />

      <ServicioFormModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setServicioEditar(null);
        }}
        onSave={handleGuardarServicio}
        servicioEditar={servicioEditar}
      />

      <ConfirmDialog
        open={servicioEliminar !== null}
        title="Eliminar Servicio"
        message={`¿Está seguro de eliminar "${servicioEliminar?.nombre ?? ""}"?`}
        onConfirm={handleEliminarServicio}
        onCancel={() =>
          setServicioEliminar(null)
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