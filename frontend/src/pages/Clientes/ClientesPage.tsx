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

const clientes = [
  {
    id: 1,
    nombre: "Juan Pérez",
    telefono: "3001234567",
    correo: "juan@gmail.com",
    estado: (
      <Chip
        label="Activo"
        color="success"
        size="small"
      />
    ),
  },
  {
    id: 2,
    nombre: "Carlos Gómez",
    telefono: "3019876543",
    correo: "carlos@gmail.com",
    estado: (
      <Chip
        label="Activo"
        color="success"
        size="small"
      />
    ),
  },
  {
    id: 3,
    nombre: "David Ramírez",
    telefono: "3205558877",
    correo: "david@gmail.com",
    estado: (
      <Chip
        label="Inactivo"
        size="small"
      />
    ),
  },
];

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
  },
];

export default function ClientesPage() {
  return (
    <Box>
      <PageHeader
        title="Clientes"
        subtitle="Administra los clientes registrados."
        buttonText="Nuevo cliente"
      />

      <TextField
        fullWidth
        placeholder="Buscar cliente..."
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
        rows={clientes}
        renderActions={() => (
          <>
            <IconButton color="primary">
              <EditIcon />
            </IconButton>

            <IconButton color="error">
              <DeleteIcon />
            </IconButton>
          </>
        )}
      />
    </Box>
  );
}