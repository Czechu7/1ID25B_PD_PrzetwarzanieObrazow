package pl.backend.user;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import pl.backend.exception.ResourceNotFoundException;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

public class UserServiceTest {

    @InjectMocks
    private UserService userService;

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void getUsersReturnsListOfUsers() {
        User user1 = new User("user1", "password", UserRole.ROLE_USER);
        User user2 = new User("user2", "password", UserRole.ROLE_USER);
        List<User> users = Arrays.asList(user1, user2);

        when(userRepository.findAll()).thenReturn(users);

        List<UserDTO> result = userService.getUsers();

        assertEquals(2, result.size());
        assertEquals("user1", result.get(0).name());
        assertEquals("user2", result.get(1).name());
    }

    @Test
    public void updateUserReturnsUpdatedUser() {
        User user = new User("user1", "password", UserRole.ROLE_USER);
        UserDTO userDTO = new UserDTO(1L, "user2", UserRole.ROLE_ADMIN);

        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userRepository.save(any(User.class))).thenAnswer(invocation -> invocation.getArgument(0));

        UserDTO result = userService.updateUser(1L, userDTO);

        assertEquals("user2", result.name());
        assertEquals(UserRole.ROLE_ADMIN, result.role());
    }

    @Test
    public void updateUserThrowsResourceNotFoundException() {
        UserDTO userDTO = new UserDTO(1L, "user1", UserRole.ROLE_USER);

        when(userRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> userService.updateUser(1L, userDTO));
    }

    @Test
    public void loadUserByUsernameReturnsUserDetails() {
        User user = new User("user1", "password", UserRole.ROLE_USER);

        when(userRepository.findByName("user1")).thenReturn(Optional.of(user));

        UserDetails result = userService.loadUserByUsername("user1");

        assertEquals("user1", result.getUsername());
    }

    @Test
    public void loadUserByUsernameThrowsResourceNotFoundException() {
        when(userRepository.findByName("userxxx")).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> userService.loadUserByUsername("userxxx"));
    }


    @Test
    public void deleteUser() {
        doNothing().when(userRepository).deleteById(1L);

        userService.deleteUser(1L);

        verify(userRepository, times(1)).deleteById(1L);
    }

    @Test
    public void createUserReturnsCreatedUser() {
        User user = new User("user1", "password", UserRole.ROLE_USER);

        when(passwordEncoder.encode(user.getPassword())).thenReturn("encodedPassword");
        when(userRepository.save(user)).thenReturn(user);

        UserDTO result = userService.createUser(user);

        assertEquals("user1", result.name());
    }
}