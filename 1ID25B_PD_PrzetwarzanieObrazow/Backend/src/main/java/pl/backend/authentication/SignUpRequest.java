package pl.backend.authentication;

public record SignUpRequest(
        String name,
        String password
) {
}
