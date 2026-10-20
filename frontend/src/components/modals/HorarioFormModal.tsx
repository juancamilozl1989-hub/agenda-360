import { useEffect, useState } from "react";

import {
  Alert,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { DIAS_SEMANA } from "../../api/tipos";
import type { Barbero, HorarioForm } from "../../api/tipos";

interface HorarioFormModalProps {
  open: boolean;
  onClose: () => void;
  // Recibe un horario por cada día elegido. Devuelve true si todo se
  // guardó; solo entonces se cierra el modal.
  onSave: (horarios: HorarioForm[]) => Promise<boolean>;
  horarioEditar?: HorarioForm | null;
  barberos: Barbero[];
}

const VACIO: HorarioForm = {
  id: 0,
  dia_semana: "",
  hora_inicio: "08:00",
  hora_fin: "18:00",
  barber_id: 0,
};

export default function HorarioFormModal({
  open,
  onClose,
  onSave,
  horarioEditar,
  barberos,
}: HorarioFormModalProps) {
  const [formData, setFormData] = useState<HorarioForm>(VACIO);
  // Al crear se pueden marcar varios días a la vez (por ejemplo, lunes a sábado)
  const [dias, setDias] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    const inicial = horarioEditar ?? VACIO;
    setFormData(inicial);
    setDias(inicial.dia_semana ? [inicial.dia_semana] : []);
    setError("");
  }, [horarioEditar, open]);

  const alternarDia = (dia: string) => {
    if (horarioEditar) {
      setDias([dia]); // al editar se cambia un solo bloque
      return;
    }
    setDias((actuales) =>
      actuales.includes(dia)
        ? actuales.filter((d) => d !== dia)
        : [...actuales, dia]
    );
  };

  const handleSave = async () => {
    if (!formData.barber_id || dias.length === 0) {
      setError("Elige el barbero y al menos un día.");
      return;
    }

    if (!formData.hora_inicio || !formData.hora_fin) {
      setError("Indica la hora de inicio y la hora de fin.");
      return;
    }

    if (formData.hora_fin <= formData.hora_inicio) {
      setError("La hora de fin debe ser posterior a la hora de inicio.");
      return;
    }

    setError("");
    setGuardando(true);
    const guardado = await onSave(
      DIAS_SEMANA.filter((d) => dias.includes(d)).map((dia) => ({
        ...formData,
        dia_semana: dia,
      }))
    );
    setGuardando(false);

    if (guardado) onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>
        {horarioEditar ? "Editar horario" : "Nuevo horario de atención"}
      </DialogTitle>

      <DialogContent>
        <Stack spacing={3} mt={1}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            select
            label="Barbero"
            value={formData.barber_id || ""}
            onChange={(e) =>
              setFormData({ ...formData, barber_id: Number(e.target.value) })
            }
            fullWidth
          >
            {barberos.map((b) => (
              <MenuItem key={b.id} value={b.id}>
                {b.nombre}
                {b.estado !== "Activo" ? " (inactivo)" : ""}
              </MenuItem>
            ))}
          </TextField>

          <Box>
            <Typography variant="body2" color="text.secondary" mb={1}>
              {horarioEditar ? "Día" : "Días (puedes marcar varios)"}
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {DIAS_SEMANA.map((dia) => {
                const activo = dias.includes(dia);
                return (
                  <Chip
                    key={dia}
                    label={dia}
                    onClick={() => alternarDia(dia)}
                    variant={activo ? "filled" : "outlined"}
                    sx={
                      activo
                        ? { bgcolor: "#D4AF37", color: "#121212", fontWeight: 600 }
                        : undefined
                    }
                  />
                );
              })}
            </Box>
          </Box>

          <Stack direction="row" spacing={2}>
            <TextField
              label="Desde"
              type="time"
              value={formData.hora_inicio}
              onChange={(e) =>
                setFormData({ ...formData, hora_inicio: e.target.value })
              }
              fullWidth
              slotProps={{ inputLabel: { shrink: true } }}
            />
            <TextField
              label="Hasta"
              type="time"
              value={formData.hora_fin}
              onChange={(e) =>
                setFormData({ ...formData, hora_fin: e.target.value })
              }
              fullWidth
              slotProps={{ inputLabel: { shrink: true } }}
            />
          </Stack>

          <Typography variant="body2" color="text.secondary">
            Si el barbero tiene jornada partida (por ejemplo, mañana y tarde),
            registra un bloque para cada parte del día.
          </Typography>
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
          {horarioEditar ? "Actualizar" : "Guardar"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
