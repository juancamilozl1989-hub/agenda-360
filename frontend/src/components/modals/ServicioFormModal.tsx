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

import type { ServicioForm } from "../../api/tipos";

interface ServicioFormModalProps {
  open: boolean;
  onClose: () => void;
  // Devuelve true si la API aceptó el cambio; solo entonces se cierra el modal.
  onSave: (servicio: ServicioForm) => Promise<boolean>;
  servicioEditar?: ServicioForm | null;
}

// Los servicios son el catálogo de la barbería: no se asignan a un
// barbero, porque cualquier barbero activo puede atenderlos.

const VACIO: ServicioForm = {
  id: 0,
  nombre: "",
  categoria: "",
  descripcion: "",
  duracion: 30,
  precio: 0,
  estado: "Activo",
  barbershop_id: 0,
};

export default function ServicioFormModal({
  open,
  onClose,
  onSave,
  servicioEditar,
}: ServicioFormModalProps) {
  const [formData, setFormData] = useState<ServicioForm>(VACIO);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    setFormData(servicioEditar ?? VACIO);
    setError("");
  }, [servicioEditar, open]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]:
        name === "duracion" || name === "precio"
          ? Number(value)
          : value,
    });
  };

  const handleSave = async () => {
    if (
      !formData.nombre.trim() ||
      !formData.categoria.trim()
    ) {
      setError("Nombre y categoría son obligatorios.");
      return;
    }

    if (formData.precio <= 0 || formData.duracion <= 0) {
      setError("El precio y la duración deben ser mayores que cero.");
      return;
    }

    setGuardando(true);
    const guardado = await onSave({
      ...formData,
      nombre: formData.nombre.trim(),
      descripcion:
        formData.descripcion.trim() || formData.nombre.trim(),
    });
    setGuardando(false);

    if (guardado) onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>
        {servicioEditar ? "Editar Servicio" : "Nuevo Servicio"}
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
            select
            label="Categoría"
            name="categoria"
            value={formData.categoria}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="Corte">Corte</MenuItem>
            <MenuItem value="Barba">Barba</MenuItem>
            <MenuItem value="Color">Color</MenuItem>
            <MenuItem value="Tratamiento">Tratamiento</MenuItem>
          </TextField>

          <TextField
            label="Descripción"
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            fullWidth
            multiline
            minRows={2}
          />

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
          {servicioEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
