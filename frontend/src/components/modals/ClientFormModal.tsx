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

export interface Cliente {
  id: number;
  nombre: string;
  telefono: string;
  correo: string;
  estado: string;
}

interface ClientFormModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (cliente: Cliente) => void;
  clienteEditar?: Cliente | null;
}

export default function ClientFormModal({
  open,
  onClose,
  onSave,
  clienteEditar,
}: ClientFormModalProps) {
  const [formData, setFormData] = useState<Cliente>({
    id: 0,
    nombre: "",
    telefono: "",
    correo: "",
    estado: "Activo",
  });

  useEffect(() => {
    if (clienteEditar) {
      setFormData(clienteEditar);
    } else {
      setFormData({
        id: 0,
        nombre: "",
        telefono: "",
        correo: "",
        estado: "Activo",
      });
    }
  }, [clienteEditar, open]);

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
      !formData.telefono.trim() ||
      !formData.correo.trim()
    ) {
      alert("Todos los campos son obligatorios.");
      return;
    }

    const cliente: Cliente = {
      ...formData,
      id:
        formData.id === 0
          ? Date.now()
          : formData.id,
    };

    onSave(cliente);
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
        {clienteEditar
          ? "Editar Cliente"
          : "Nuevo Cliente"}
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
            label="Teléfono"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
            fullWidth
          />

          <TextField
            label="Correo electrónico"
            name="correo"
            value={formData.correo}
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
          {clienteEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}