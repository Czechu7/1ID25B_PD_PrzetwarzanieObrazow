package pl.backend.user;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(1)
@RequiredArgsConstructor
public class UserCommandLine implements CommandLineRunner {
    private final UserService userService;

    @Override
    public void run(String... args) throws Exception {
        userService.createUser(new User("admin", "admin", UserRole.ROLE_ADMIN));
    }
}
