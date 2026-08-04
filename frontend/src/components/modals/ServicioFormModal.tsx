import { useEffect, useState } from "react";

import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";

export interface Servicio {
  id: number;
  nombre: string;
  categoria: string;
  duracion: number;
  precio: number;
  estado: string;
}

interface ServicioFormModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (servicio: Servicio) => void;
  servicioEditar?: Servicio | null;
}

export default function ServicioFormModal({
  open,
  onClose,
  onSave,
  servicioEditar,
}: ServicioFormModalProps) {
  const [formData, setFormData] =
    useState<Servicio>({
      id: 0,
      nombre: "",
      categoria: "",
      duracion: 30,
      precio: 0,
      estado: "Activo",
    });

  useEffect(() => {
    if (servicioEditar) {
      setFormData(servicioEditar);
    } else {
      setFormData({
        id: 0,
        nombre: "",
        categoria: "",
        duracion: 30,
        precio: 0,
        estado: "Activo",
      });
    }
  }, [servicioEditar, open]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]:
        e.target.name === "duracion" ||
        e.target.name === "precio"
          ? Number(e.target.value)
          : e.target.value,
    });
  };

  const handleSave = () => {
    if (
      !formData.nombre.trim() ||
      !formData.categoria.trim()
    ) {
      alert("Todos los campos son obligatorios.");
      return;
    }

    onSave({
      ...formData,
      id:
        formData.id === 0
          ? Date.now()
          : formData.id,
    });

    onClose();
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
    >
      <DialogTitle>
        {servicioEditar
          ? "Editar Servicio"
          : "Nuevo Servicio"}
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3} mt={1}>
          <TextField
            label="Nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            select
            label="Categoría"
            name="categoria"
            value={formData.categoria}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="Corte">
              Corte
            </MenuItem>

            <MenuItem value="Barba">
              Barba
            </MenuItem>

            <MenuItem value="Color">
              Color
            </MenuItem>

            <MenuItem value="Tratamiento">
              Tratamiento
            </MenuItem>
          </TextField>

          <TextField
            label="Duración (min)"
            name="duracion"
            type="number"
            value={formData.duracion}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            label="Precio"
            name="precio"
            type="number"
            value={formData.precio}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            select
            label="Estado"
            name="estado"
            value={formData.estado}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="Activo">
              Activo
            </MenuItem>

            <MenuItem value="Inactivo">
              Inactivo
            </MenuItem>
          </TextField>
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose}>
          Cancelar
        </Button>

        <Button
          variant="contained"
          onClick={handleSave}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            "&:hover": {
              bgcolor: "#C49A1D",
            },
          }}
        >
          {servicioEditar
            ? "Actualizar"
            : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}