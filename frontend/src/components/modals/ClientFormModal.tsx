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

import type { ClienteForm } from "../../api/tipos";

interface ClientFormModalProps {
  open: boolean;
  onClose: () => void;
  // Devuelve true si la API aceptó el cambio; solo entonces se cierra el modal.
  onSave: (cliente: ClienteForm) => Promise<boolean>;
  clienteEditar?: ClienteForm | null;
}

const VACIO: ClienteForm = {
  id: 0,
  nombre: "",
  telefono: "",
  email: "",
  estado: "Activo",
};

export default function ClientFormModal({
  open,
  onClose,
  onSave,
  clienteEditar,
}: ClientFormModalProps) {
  const [formData, setFormData] = useState<ClienteForm>(VACIO);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    setFormData(clienteEditar ?? VACIO);
    setError("");
  }, [clienteEditar, open]);

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
      !formData.telefono.trim() ||
      !formData.email.trim()
    ) {
      setError("Todos los campos son obligatorios.");
      return;
    }

    setGuardando(true);
    const guardado = await onSave({
      ...formData,
      nombre: formData.nombre.trim(),
      telefono: formData.telefono.trim(),
      email: formData.email.trim(),
    });
    setGuardando(false);

    if (guardado) onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>
        {clienteEditar ? "Editar Cliente" : "Nuevo Cliente"}
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
            label="Teléfono"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            label="Correo electrónico"
            name="email"
            type="email"
            value={formData.email}
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
          {clienteEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
