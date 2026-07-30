import { Box, Button, Typography } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import type { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  subtitle: string;
  buttonText?: string;
  buttonIcon?: ReactNode;
  onClick?: () => void;
}

export default function PageHeader({
  title,
  subtitle,
  buttonText,
  buttonIcon = <AddIcon />,
  onClick,
}: PageHeaderProps) {
  return (
    <Box
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      mb={4}
    >
      <Box>
        <Typography variant="h4" fontWeight="bold">
          {title}
        </Typography>

        <Typography color="text.secondary">
          {subtitle}
        </Typography>
      </Box>

      {buttonText && (
        <Button
          variant="contained"
          startIcon={buttonIcon}
          onClick={onClick}
          sx={{
            bgcolor: "#D4AF37",
            color: "#121212",
            fontWeight: "bold",
            borderRadius: 3,
            px: 3,
            "&:hover": {
              bgcolor: "#C49A1D",
            },
          }}
        >
          {buttonText}
        </Button>
      )}
    </Box>
  );
}