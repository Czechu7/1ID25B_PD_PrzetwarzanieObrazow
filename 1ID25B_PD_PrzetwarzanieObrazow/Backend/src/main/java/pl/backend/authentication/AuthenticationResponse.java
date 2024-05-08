package pl.backend.authentication;

import pl.backend.user.UserDTO;

public record AuthenticationResponse(
    String token,
    UserDTO user
)
{}
