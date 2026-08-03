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

const servicios = [
  {
    id: 1,
    nombre: "Corte Clásico",
    duracion: "30 min",
    precio: "$25.000",
    estado: (
      <Chip
        label="Disponible"
        color="success"
        size="small"
      />
    ),
  },
  {
    id: 2,
    nombre: "Fade Premium",
    duracion: "45 min",
    precio: "$35.000",
    estado: (
      <Chip
        label="Disponible"
        color="success"
        size="small"
      />
    ),
  },
  {
    id: 3,
    nombre: "Barba",
    duracion: "20 min",
    precio: "$18.000",
    estado: (
      <Chip
        label="Disponible"
        color="success"
        size="small"
      />
    ),
  },
  {
    id: 4,
    nombre: "Corte + Barba",
    duracion: "60 min",
    precio: "$45.000",
    estado: (
      <Chip
        label="Promoción"
        color="warning"
        size="small"
      />
    ),
  },
];

const columns = [
  {
    field: "nombre",
    headerName: "Servicio",
  },
  {
    field: "duracion",
    headerName: "Duración",
  },
  {
    field: "precio",
    headerName: "Precio",
  },
  {
    field: "estado",
    headerName: "Estado",
  },
];

export default function ServiciosPage() {
  return (
    <Box>
      <PageHeader
        title="Servicios"
        subtitle="Administra el catálogo de servicios."
        buttonText="Nuevo Servicio"
      />

      <TextField
        fullWidth
        placeholder="Buscar servicio..."
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
        rows={servicios}
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