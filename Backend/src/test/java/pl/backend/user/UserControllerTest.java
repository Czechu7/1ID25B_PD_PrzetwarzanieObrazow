package pl.backend.user;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;

public class UserControllerTest {

    @InjectMocks
    private UserController userController;

    @Mock
    private UserService userService;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void getUsersReturnsListOfUsers() {
        UserDTO user1 = new UserDTO(1L, "user1", UserRole.ROLE_USER);
        UserDTO user2 = new UserDTO(2L, "user2", UserRole.ROLE_USER);
        List<UserDTO> users = Arrays.asList(user1, user2);

        when(userService.getUsers()).thenReturn(users);

        ResponseEntity<List<UserDTO>> response = userController.getUser();

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(users, response.getBody());
    }

    @Test
    public void updateUserReturnsUpdatedUser() {
        UserDTO user = new UserDTO(1L, "user1", UserRole.ROLE_USER);

        when(userService.updateUser(1L, user)).thenReturn(user);

        ResponseEntity<UserDTO> response = userController.updateUser(1L, user);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(user, response.getBody());
    }

    @Test
    public void deleteUserReturnsNoContent() {
        doNothing().when(userService).deleteUser(1L);

        ResponseEntity<Void> response = userController.deleteUser(1L);

        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
    }
}