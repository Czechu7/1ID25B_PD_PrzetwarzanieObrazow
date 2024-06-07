package pl.backend.classifiedImages;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;
import pl.backend.jwt.JWTUtil;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class ClassifiedImagesControllerTest {

    @Mock
    private JWTUtil authenticationService;

    @Mock
    private ClassifiedImagesService classifiedImagesService;

    @InjectMocks
    private ClassifiedImagesController classifiedImagesController;

    @Test
    public void uploadImageReturnsCreated() throws Exception {
        String token = "Bearer token";
        String userId = "user1";
        MultipartFile file = new MockMultipartFile("image", "image.jpg", "image/jpeg", "image".getBytes());
        String classifiedText = "classifiedText";
        String userText = "userText";

        when(authenticationService.getId(anyString())).thenReturn(userId);

        ResponseEntity<String> response = classifiedImagesController.uploadImage(file, classifiedText, userText, token);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
    }

    @Test
    public void getAllImagesForUserReturnsImages() {
        String token = "Bearer token";
        String userId = "user1";
        ClassifiedImagesUser classifiedImagesUser = new ClassifiedImagesUser();
        List<ClassifiedImagesUser> expectedImages = Collections.singletonList(classifiedImagesUser);

        when(authenticationService.getId(anyString())).thenReturn(userId);
        when(classifiedImagesService.getAllImagesForUser(userId)).thenReturn(expectedImages);

        ResponseEntity<?> response = classifiedImagesController.getAllImagesForUser(userId, token);

        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    @Test
    public void getImageForUserReturnsImageData() {
        String token = "Bearer token";
        String userId = "user1";
        String imageName = "image1";
        ClassifiedImagesUser classifiedImagesUser = new ClassifiedImagesUser();
        classifiedImagesUser.setImageData(new byte[]{1, 2, 3});

        when(authenticationService.getId(anyString())).thenReturn(userId);
        when(classifiedImagesService.getImageData(userId, imageName)).thenReturn(new ResponseEntity<>(classifiedImagesUser.getImageData(), HttpStatus.OK));

        ResponseEntity<byte[]> response = classifiedImagesController.getImageForUser(userId, imageName, token);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(classifiedImagesUser.getImageData(), response.getBody());
    }
}