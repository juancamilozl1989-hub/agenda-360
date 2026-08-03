import {
  Box,
  Chip,
  IconButton,
  InputAdornment,
  TextField,
  Avatar,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/tables/DataTable";

const barberos = [
  {
    id: 1,
    foto: (
      <Avatar sx={{ bgcolor: "#D4AF37", color: "#121212" }}>
        C
      </Avatar>
    ),
    nombre: "Carlos Gómez",
    especialidad: "Fade / Barba",
    telefono: "3001234567",
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
    foto: (
      <Avatar sx={{ bgcolor: "#3B82F6" }}>
        J
      </Avatar>
    ),
    nombre: "Juan Pérez",
    especialidad: "Corte clásico",
    telefono: "3019876543",
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
    foto: (
      <Avatar sx={{ bgcolor: "#EF4444" }}>
        D
      </Avatar>
    ),
    nombre: "David Ramírez",
    especialidad: "Colorista",
    telefono: "3204567890",
    estado: (
      <Chip
        label="Vacaciones"
        color="warning"
        size="small"
      />
    ),
  },
];

const columns = [
  {
    field: "foto",
    headerName: "",
  },
  {
    field: "nombre",
    headerName: "Barbero",
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
  },
];

export default function BarberosPage() {
  return (
    <Box>
      <PageHeader
        title="Barberos"
        subtitle="Administra el equipo de trabajo."
        buttonText="Nuevo Barbero"
      />

      <TextField
        fullWidth
        placeholder="Buscar barbero..."
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
        rows={barberos}
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