package pl.backend.user;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import pl.backend.exception.ResourceNotFoundException;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService implements UserDetailsService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;


    public List<UserDTO> getUsers() {
        return userRepository.findAll().stream().map(UserMapper::mapToUserDTO).toList();
    }

    public UserDTO updateUser(Long id, UserDTO user) {
        User userToUpdate = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User with id [%s] found".formatted(id)));

        if(user.role() != null) {
            userToUpdate.setUserRole(user.role());
        }
        return UserMapper.mapToUserDTO(userRepository.save(userToUpdate));
    }


    @Override
    public UserDetails loadUserByUsername(String name) throws UsernameNotFoundException {
        return userRepository.findByName(name)
                .orElseThrow(() -> new ResourceNotFoundException("User with email [%s] not found".formatted(name)));
    }

    public User getUserByName(String name){
        return userRepository.findByName(name)
                .orElseThrow(() -> new ResourceNotFoundException("User with email [%s] not found".formatted(name)));
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }

    public UserDTO createUser(User user) {
        String encodedPassword = passwordEncoder.encode(user.getPassword());
        user.setPassword(encodedPassword);
        return UserMapper.mapToUserDTO(userRepository.save(user));
    }
}
