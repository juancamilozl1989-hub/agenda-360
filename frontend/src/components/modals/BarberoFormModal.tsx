import { useEffect, useState } from "react";

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Stack,
  TextField,
  MenuItem,
} from "@mui/material";

export interface Barbero {
  id: number;
  nombre: string;
  especialidad: string;
  telefono: string;
  estado: string;
}

interface BarberoFormModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (barbero: Barbero) => void;
  barberoEditar?: Barbero | null;
}

export default function BarberoFormModal({
  open,
  onClose,
  onSave,
  barberoEditar,
}: BarberoFormModalProps) {
  const [formData, setFormData] = useState<Barbero>({
    id: 0,
    nombre: "",
    especialidad: "",
    telefono: "",
    estado: "Activo",
  });

  useEffect(() => {
    if (barberoEditar) {
      setFormData(barberoEditar);
    } else {
      setFormData({
        id: 0,
        nombre: "",
        especialidad: "",
        telefono: "",
        estado: "Activo",
      });
    }
  }, [barberoEditar, open]);

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSave = () => {
    if (
      !formData.nombre.trim() ||
      !formData.especialidad.trim() ||
      !formData.telefono.trim()
    ) {
      alert("Todos los campos son obligatorios.");
      return;
    }

    const nuevoBarbero: Barbero = {
      ...formData,
      id:
        formData.id === 0
          ? Date.now()
          : formData.id,
    };

    onSave(nuevoBarbero);
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
        {barberoEditar
          ? "Editar Barbero"
          : "Nuevo Barbero"}
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
            label="Especialidad"
            name="especialidad"
            value={formData.especialidad}
            onChange={handleChange}
            fullWidth
            placeholder="Ej: Fade, Barba, Color..."
          />

          <TextField
            label="Teléfono"
            name="telefono"
            value={formData.telefono}
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
          {barberoEditar
            ? "Actualizar"
            : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}