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

import ClientFormModal from "../../components/modals/ClientFormModal";
import type { Cliente } from "../../components/modals/ClientFormModal";

export default function ClientesPage() {
  const [openModal, setOpenModal] = useState(false);

  const [clienteEditar, setClienteEditar] =
    useState<Cliente | null>(null);

  const [clienteEliminar, setClienteEliminar] =
    useState<Cliente | null>(null);

  const [busqueda, setBusqueda] = useState("");

  const [clientes, setClientes] = useState<Cliente[]>([
    {
      id: 1,
      nombre: "Juan Pérez",
      telefono: "3001234567",
      correo: "juan@gmail.com",
      estado: "Activo",
    },
    {
      id: 2,
      nombre: "Carlos Gómez",
      telefono: "3019876543",
      correo: "carlos@gmail.com",
      estado: "Activo",
    },
    {
      id: 3,
      nombre: "David Ramírez",
      telefono: "3205558877",
      correo: "david@gmail.com",
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

  const clientesFiltrados = useMemo(() => {
    return clientes.filter((cliente) => {
      const texto = busqueda.toLowerCase();

      return (
        cliente.nombre.toLowerCase().includes(texto) ||
        cliente.telefono.includes(texto) ||
        cliente.correo.toLowerCase().includes(texto)
      );
    });
  }, [clientes, busqueda]);

  const handleNuevoCliente = () => {
    setClienteEditar(null);
    setOpenModal(true);
  };

  const handleEditarCliente = (
    cliente: Cliente
  ) => {
    setClienteEditar(cliente);
    setOpenModal(true);
  };

  const handleGuardarCliente = (
    cliente: Cliente
  ) => {
    const existe = clientes.some(
      (c) => c.id === cliente.id
    );

    if (existe) {
      setClientes(
        clientes.map((c) =>
          c.id === cliente.id ? cliente : c
        )
      );

      setSnackbar({
        open: true,
        message:
          "Cliente actualizado correctamente.",
        severity: "success",
      });
    } else {
      setClientes([...clientes, cliente]);

      setSnackbar({
        open: true,
        message:
          "Cliente creado correctamente.",
        severity: "success",
      });
    }

    setClienteEditar(null);
  };

  const handleEliminarCliente = () => {
    if (!clienteEliminar) return;

    setClientes(
      clientes.filter(
        (c) => c.id !== clienteEliminar.id
      )
    );

    setSnackbar({
      open: true,
      message:
        "Cliente eliminado correctamente.",
      severity: "success",
    });

    setClienteEliminar(null);
  };

  const columns = [
    {
      field: "nombre",
      headerName: "Nombre",
    },
    {
      field: "telefono",
      headerName: "Teléfono",
    },
    {
      field: "correo",
      headerName: "Correo",
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
        title="Clientes"
        subtitle="Administra los clientes registrados."
        buttonText="Nuevo Cliente"
        onClick={handleNuevoCliente}
      />

      <TextField
        fullWidth
        placeholder="Buscar cliente..."
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
        rows={clientesFiltrados}
        renderActions={(row) => (
          <>
            <IconButton
              color="primary"
              onClick={() =>
                handleEditarCliente(row)
              }
            >
              <EditIcon />
            </IconButton>

            <IconButton
              color="error"
              onClick={() =>
                setClienteEliminar(row)
              }
            >
              <DeleteIcon />
            </IconButton>
          </>
        )}
      />

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
        onCancel={() =>
          setClienteEliminar(null)
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