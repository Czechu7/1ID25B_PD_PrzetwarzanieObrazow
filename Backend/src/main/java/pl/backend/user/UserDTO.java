package pl.backend.user;

public record UserDTO(
         Long id,
         String name,
         UserRole role
) {
}
