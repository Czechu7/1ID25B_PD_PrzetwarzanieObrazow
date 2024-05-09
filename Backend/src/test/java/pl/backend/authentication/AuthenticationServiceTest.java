package pl.backend.authentication;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import pl.backend.exception.UserAlreadyExistsException;
import pl.backend.jwt.JWTUtil;
import pl.backend.user.User;
import pl.backend.user.UserDTO;
import pl.backend.user.UserService;
import pl.backend.user.UserRole;

import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

public class AuthenticationServiceTest {

    @InjectMocks
    private AuthenticationService authenticationService;

    @Mock
    private AuthenticationManager authenticationManager;

    @Mock
    private UserService userService;

    @Mock
    private JWTUtil jwtUtil;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void signInWithValidRequestReturnsAuthenticationResponse() {
        SignInRequest validRequest = new SignInRequest("validUser", "validPassword");
        User principal = new User("validUser", "validPassword", UserRole.ROLE_USER);
        principal.setId(1L);
        Authentication authentication = new UsernamePasswordAuthenticationToken(principal, null);
        UserDTO userDTO = new UserDTO(principal.getId(), principal.getName(), principal.getUserRole());
        AuthenticationResponse expectedResponse = new AuthenticationResponse(null, userDTO);

        when(authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(validRequest.name(), validRequest.password()))).thenReturn(authentication);
        when(jwtUtil.issueToken(validRequest.name(), authentication.getAuthorities().stream().map(a -> a.getAuthority()).collect(Collectors.toList()))).thenReturn("validToken");

        AuthenticationResponse response = authenticationService.signin(validRequest);

        assertEquals(expectedResponse, response);
    }

    @Test
    public void signUpWithValidRequestReturnsAuthenticationResponse() {
        SignUpRequest validRequest = new SignUpRequest("validUser123", "validPassword");
        User user = new User(validRequest.name(), validRequest.password(), UserRole.ROLE_USER);
        user.setId(1L);
        UserDTO userDTO = new UserDTO(user.getId(), user.getName(), user.getUserRole());
        AuthenticationResponse expectedResponse = new AuthenticationResponse("validToken", userDTO);

        when(userService.getUserByName(validRequest.name())).thenReturn(true);
        when(userService.createUser(user)).thenReturn(userDTO);
        when(jwtUtil.issueToken(validRequest.name(), user.getAuthorities().stream().map(a -> a.getAuthority()).collect(Collectors.toList()))).thenReturn("validToken");

        AuthenticationResponse response = authenticationService.signup(validRequest);

        assertEquals(expectedResponse, response);
    }


}