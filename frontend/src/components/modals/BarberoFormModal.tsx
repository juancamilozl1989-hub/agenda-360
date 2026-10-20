import { useEffect, useState } from "react";

import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";

import type { BarberoForm } from "../../api/tipos";

interface BarberoFormModalProps {
  open: boolean;
  onClose: () => void;
  // Devuelve true si la API aceptó el cambio; solo entonces se cierra el modal.
  onSave: (barbero: BarberoForm) => Promise<boolean>;
  barberoEditar?: BarberoForm | null;
}

const VACIO: BarberoForm = {
  id: 0,
  nombre: "",
  especialidad: "",
  telefono: "",
  estado: "Activo",
};

export default function BarberoFormModal({
  open,
  onClose,
  onSave,
  barberoEditar,
}: BarberoFormModalProps) {
  const [formData, setFormData] = useState<BarberoForm>(VACIO);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    setFormData(barberoEditar ?? VACIO);
    setError("");
  }, [barberoEditar, open]);

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSave = async () => {
    if (
      !formData.nombre.trim() ||
      !formData.especialidad.trim() ||
      !formData.telefono.trim()
    ) {
      setError("Todos los campos son obligatorios.");
      return;
    }

    setGuardando(true);
    const guardado = await onSave({
      ...formData,
      nombre: formData.nombre.trim(),
      especialidad: formData.especialidad.trim(),
      telefono: formData.telefono.trim(),
    });
    setGuardando(false);

    if (guardado) onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>
        {barberoEditar ? "Editar Barbero" : "Nuevo Barbero"}
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3} mt={1}>
          {error && <Alert severity="error">{error}</Alert>}

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
            <MenuItem value="Activo">Activo</MenuItem>
            <MenuItem value="Inactivo">Inactivo</MenuItem>
          </TextField>
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button onClick={onClose}>Cancelar</Button>

        <Button
          variant="contained"
          onClick={handleSave}
          disabled={guardando}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            "&:hover": { bgcolor: "#C49A1D" },
          }}
        >
          {barberoEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
