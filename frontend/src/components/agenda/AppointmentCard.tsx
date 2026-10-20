import {
  Avatar,
  Box,
  IconButton,
  Paper,
  Typography,
} from "@mui/material";

import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

import AppointmentStatus from "./AppointmentStatus";
import type { EstadoCita } from "../../api/tipos";

interface AppointmentCardProps {
  hour: string;
  date?: string;
  client: string;
  barber: string;
  service: string;
  status: EstadoCita;
  onEdit?: () => void;
  onDelete?: () => void;
}

export default function AppointmentCard({
  hour,
  date,
  client,
  barber,
  service,
  status,
  onEdit,
  onDelete,
}: AppointmentCardProps) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2.5,
        mb: 2,
        borderRadius: 4,
        bgcolor: "#232323",
        border: "1px solid rgba(255,255,255,.08)",
        transition: ".3s",

        "&:hover": {
          transform: "translateY(-2px)",
          borderColor: "#D4AF37",
          boxShadow: "0 10px 25px rgba(0,0,0,.35)",
        },
      }}
    >
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
      >
        {/* Hora (y fecha cuando se listan varios días) */}
        <Box sx={{ width: 110 }}>
          <Typography
            sx={{ color: "#D4AF37", fontWeight: "bold" }}
          >
            {hour}
          </Typography>

          {date && (
            <Typography variant="caption" color="#888">
              {date}
            </Typography>
          )}
        </Box>

        {/* Información */}
        <Box
          display="flex"
          alignItems="center"
          flex={1}
          gap={2}
        >
          <Avatar
            sx={{
              bgcolor: "#2E2E2E",
              color: "#D4AF37",
            }}
          >
            {client.charAt(0)}
          </Avatar>

          <Box>
            <Typography fontWeight="bold" color="#FFF">
              {client}
            </Typography>

            <Typography variant="body2" color="#AAA">
              {service}
            </Typography>

            <Typography variant="caption" color="#888">
              Barbero: {barber}
            </Typography>
          </Box>
        </Box>

        {/* Estado y acciones */}
        <Box display="flex" alignItems="center" gap={1}>
          <AppointmentStatus status={status} />

          {onEdit && (
            <IconButton color="primary" onClick={onEdit}>
              <EditIcon />
            </IconButton>
          )}

          {onDelete && (
            <IconButton color="error" onClick={onDelete}>
              <DeleteIcon />
            </IconButton>
          )}
        </Box>
      </Box>
    </Paper>
  );
}
