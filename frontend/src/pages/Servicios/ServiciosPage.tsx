import { useCallback, useEffect, useMemo, useState } from "react";

import {
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
import ServicioFormModal from "../../components/modals/ServicioFormModal";

import {
  actualizarServicio,
  crearServicio,
  eliminarServicio,
  listarServicios,
} from "../../api/serviciosService";
import { mensajeError } from "../../api/errores";
import type { Servicio, ServicioForm } from "../../api/tipos";

export default function ServiciosPage() {
  const [openModal, setOpenModal] = useState(false);
  const [servicioEditar, setServicioEditar] =
    useState<ServicioForm | null>(null);
  const [servicioEliminar, setServicioEliminar] =
    useState<Servicio | null>(null);
  const [busqueda, setBusqueda] = useState("");
  const [servicios, setServicios] = useState<Servicio[]>([]);
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

  // Los servicios son el catálogo de la barbería: cualquier
  // barbero activo puede atenderlos.
  const cargarDatos = useCallback(async () => {
    try {
      setServicios(await listarServicios());
    } catch (error) {
      avisar(mensajeError(error, "No se pudieron cargar los servicios."), "error");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]);

  const serviciosFiltrados = useMemo(() => {
    const texto = busqueda.toLowerCase();

    return servicios.filter(
      (s) =>
        s.nombre.toLowerCase().includes(texto) ||
        s.categoria.toLowerCase().includes(texto)
    );
  }, [servicios, busqueda]);

  const handleGuardarServicio = async (
    form: ServicioForm
  ): Promise<boolean> => {
    try {
      if (form.id === 0) {
        await crearServicio(form);
        avisar("Servicio creado correctamente.");
      } else {
        await actualizarServicio(form);
        avisar("Servicio actualizado correctamente.");
      }

      setServicioEditar(null);
      await cargarDatos();
      return true;
    } catch (error) {
      avisar(mensajeError(error, "No se pudo guardar el servicio."), "error");
      return false;
    }
  };

  const handleEliminarServicio = async () => {
    if (!servicioEliminar) return;

    try {
      await eliminarServicio(servicioEliminar.id);
      avisar("Servicio eliminado correctamente.");
      await cargarDatos();
    } catch (error) {
      avisar(mensajeError(error, "No se pudo eliminar el servicio."), "error");
    } finally {
      setServicioEliminar(null);
    }
  };

  const columns = [
    { field: "nombre", headerName: "Servicio" },
    { field: "categoria", headerName: "Categoría" },
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
          color={value === "Activo" ? "success" : "default"}
          size="small"
        />
      ),
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Servicios"
        subtitle="Catálogo de servicios de la barbería. Cualquier barbero activo puede atenderlos."
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
          rows={serviciosFiltrados}
          renderActions={(row) => (
            <>
              <IconButton
                color="primary"
                onClick={() => {
                  setServicioEditar({
                    id: row.id,
                    nombre: row.nombre,
                    categoria: row.categoria,
                    descripcion: row.descripcion,
                    duracion: row.duracion,
                    precio: row.precio,
                    estado: row.estado,
                    barbershop_id: row.barbershop.id,
                  });
                  setOpenModal(true);
                }}
              >
                <EditIcon />
              </IconButton>

              <IconButton
                color="error"
                onClick={() => setServicioEliminar(row)}
              >
                <DeleteIcon />
              </IconButton>
            </>
          )}
        />
      )}

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
        message={`¿Está seguro de eliminar ${
          servicioEliminar?.nombre ?? ""
        }?`}
        onConfirm={handleEliminarServicio}
        onCancel={() => setServicioEliminar(null)}
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
