import {
  TextField,
  InputAdornment,
} from "@mui/material";

import type { TextFieldProps } from "@mui/material";

type Props = TextFieldProps & {
  icon?: React.ReactNode;
};

export default function CustomTextField({
  icon,
  sx,
  ...props
}: Props) {
  return (
    <TextField
      {...props}
      fullWidth
      slotProps={{
        input: {
          startAdornment: icon ? (
            <InputAdornment position="start">
              {icon}
            </InputAdornment>
          ) : undefined,
        },
      }}
      sx={{
        mb: 2,

        "& .MuiOutlinedInput-root": {
          color: "#fff",

          "& fieldset": {
            borderColor: "#555",
          },

          "&:hover fieldset": {
            borderColor: "#D4AF37",
          },

          "&.Mui-focused fieldset": {
            borderColor: "#D4AF37",
          },
        },

        "& .MuiInputLabel-root": {
          color: "#aaa",
        },

        "& .MuiInputLabel-root.Mui-focused": {
          color: "#D4AF37",
        },

        ...sx,
      }}
    />
  );
}