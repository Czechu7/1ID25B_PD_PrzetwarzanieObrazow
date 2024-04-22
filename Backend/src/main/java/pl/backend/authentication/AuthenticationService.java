package pl.backend.authentication;

import pl.backend.jwt.JWTUtil;
import pl.backend.user.*;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.security.core.GrantedAuthority;


import java.util.stream.Collectors;

@RequiredArgsConstructor
@Service

public class AuthenticationService {
    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final JWTUtil jwtUtil;

    public AuthenticationResponse signin(SignInRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.name(),
                        request.password()
                )
        );
        User principal = (User) authentication.getPrincipal();
        UserDTO userDTO = new UserDTO(
                principal.getId(),
                principal.getName(),
                principal.getUserRole()
        );

        String token = jwtUtil.issueToken(
                principal.getName(),
                principal.getAuthorities()
                        .stream()
                        .map(GrantedAuthority::getAuthority)
                        .collect(Collectors.toList()));
        return new AuthenticationResponse(token, userDTO);
    }

    public AuthenticationResponse signup(SignUpRequest signUpRequest) {

        System.out.println(signUpRequest.name());
        User user = new User(signUpRequest.name(), signUpRequest.password(), UserRole.ROLE_USER);




        UserDTO userDTO =  userService.createUser(user);
        String token = jwtUtil.issueToken( user.getName(), user.getAuthorities()
                .stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.toList()));

        return new AuthenticationResponse(token, userDTO);
    }
}
