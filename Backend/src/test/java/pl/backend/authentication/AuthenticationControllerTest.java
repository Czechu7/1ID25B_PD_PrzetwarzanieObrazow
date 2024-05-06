package pl.backend.authentication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

public class AuthenticationControllerTest {

    @InjectMocks
    private AuthenticationController authenticationController;

    @Mock
    private AuthenticationService authenticationService;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void signInWithValidRequestReturnsOkStatus() {
        SignInRequest validRequest = new SignInRequest("validUser", "validPassword");
        AuthenticationResponse expectedResponse = new AuthenticationResponse("validToken", null);

        when(authenticationService.signin(validRequest)).thenReturn(expectedResponse);

        ResponseEntity<AuthenticationResponse> responseEntity = authenticationController.signin(validRequest);

        assertEquals(HttpStatus.OK, responseEntity.getStatusCode());
        assertEquals(expectedResponse, responseEntity.getBody());
    }

    @Test
    public void signUpWithValidRequestReturnsCreatedStatus() {
        SignUpRequest validRequest = new SignUpRequest("validUser", "validPassword");
        AuthenticationResponse expectedResponse = new AuthenticationResponse("validToken", null);

        when(authenticationService.signup(validRequest)).thenReturn(expectedResponse);

        ResponseEntity<AuthenticationResponse> responseEntity = authenticationController.signup(validRequest);

        assertEquals(HttpStatus.CREATED, responseEntity.getStatusCode());
        assertEquals(expectedResponse, responseEntity.getBody());
    }

    @Test
    public void signInWithInvalidRequestThrowsException() {
        SignInRequest invalidRequest = new SignInRequest("", "");

        assertThrows(IllegalArgumentException.class, () -> authenticationController.signin(invalidRequest));
    }

    @Test
    public void signUpWithInvalidRequestThrowsException() {
        SignUpRequest invalidRequest = new SignUpRequest("", "");

        assertThrows(IllegalArgumentException.class, () -> authenticationController.signup(invalidRequest));
    }
}
