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
import ClientFormModal from "../../components/modals/ClientFormModal";

import {
  actualizarCliente,
  crearCliente,
  eliminarCliente,
  listarClientes,
} from "../../api/clientesService";
import { obtenerBarberiaPrincipal } from "../../api/barberiasService";
import { mensajeError } from "../../api/errores";
import type { Cliente, ClienteForm } from "../../api/tipos";

export default function ClientesPage() {
  const [openModal, setOpenModal] = useState(false);
  const [clienteEditar, setClienteEditar] =
    useState<ClienteForm | null>(null);
  const [clienteEliminar, setClienteEliminar] =
    useState<Cliente | null>(null);
  const [busqueda, setBusqueda] = useState("");
  const [clientes, setClientes] = useState<Cliente[]>([]);
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

  // Carga inicial desde la API
  const cargarClientes = useCallback(async () => {
    try {
      setClientes(await listarClientes());
    } catch (error) {
      avisar(mensajeError(error, "No se pudieron cargar los clientes."), "error");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargarClientes();
  }, [cargarClientes]);

  const clientesFiltrados = useMemo(() => {
    const texto = busqueda.toLowerCase();

    return clientes.filter(
      (cliente) =>
        cliente.nombre.toLowerCase().includes(texto) ||
        cliente.telefono.includes(texto) ||
        cliente.email.toLowerCase().includes(texto)
    );
  }, [clientes, busqueda]);

  const handleEditarCliente = (cliente: Cliente) => {
    setClienteEditar({
      id: cliente.id,
      nombre: cliente.nombre,
      telefono: cliente.telefono,
      email: cliente.email,
      estado: cliente.estado,
    });
    setOpenModal(true);
  };

  // Crea o actualiza según el id y devuelve si la operación fue exitosa
  const handleGuardarCliente = async (
    form: ClienteForm
  ): Promise<boolean> => {
    try {
      const barberia = await obtenerBarberiaPrincipal();

      if (form.id === 0) {
        await crearCliente(form, barberia.id);
        avisar("Cliente creado correctamente.");
      } else {
        await actualizarCliente(form, barberia.id);
        avisar("Cliente actualizado correctamente.");
      }

      setClienteEditar(null);
      await cargarClientes();
      return true;
    } catch (error) {
      avisar(mensajeError(error, "No se pudo guardar el cliente."), "error");
      return false;
    }
  };

  const handleEliminarCliente = async () => {
    if (!clienteEliminar) return;

    try {
      await eliminarCliente(clienteEliminar.id);
      avisar("Cliente eliminado correctamente.");
      await cargarClientes();
    } catch (error) {
      avisar(mensajeError(error, "No se pudo eliminar el cliente."), "error");
    } finally {
      setClienteEliminar(null);
    }
  };

  const columns = [
    { field: "nombre", headerName: "Nombre" },
    { field: "telefono", headerName: "Teléfono" },
    { field: "email", headerName: "Correo" },
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
        title="Clientes"
        subtitle="Administra los clientes registrados."
        buttonText="Nuevo Cliente"
        onClick={() => {
          setClienteEditar(null);
          setOpenModal(true);
        }}
      />

      <TextField
        fullWidth
        placeholder="Buscar cliente..."
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
          rows={clientesFiltrados}
          renderActions={(row) => (
            <>
              <IconButton
                color="primary"
                onClick={() => handleEditarCliente(row)}
              >
                <EditIcon />
              </IconButton>

              <IconButton
                color="error"
                onClick={() => setClienteEliminar(row)}
              >
                <DeleteIcon />
              </IconButton>
            </>
          )}
        />
      )}

      <ClientFormModal
        open={openModal}
        onClose={() => {
          setOpenModal(false);
          setClienteEditar(null);
        }}
        onSave={handleGuardarCliente}
        clienteEditar={clienteEditar}
      />

      <ConfirmDialog
        open={clienteEliminar !== null}
        title="Eliminar Cliente"
        message={`¿Está seguro de eliminar a ${
          clienteEliminar?.nombre ?? ""
        }?`}
        onConfirm={handleEliminarCliente}
        onCancel={() => setClienteEliminar(null)}
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
