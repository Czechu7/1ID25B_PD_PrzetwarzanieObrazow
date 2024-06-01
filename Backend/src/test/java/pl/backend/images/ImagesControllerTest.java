package pl.backend.images;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;
import pl.backend.jwt.JWTUtil;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class ImagesControllerTest {

    @Mock
    private JWTUtil jwtUtil;

    @InjectMocks
    private ImagesController imagesController;

    private String targetFolder = "targetFolder";



    @Test
    public void uploadImageReturnsBadRequestWhenFileIsEmpty() throws Exception {
        MultipartFile file = new MockMultipartFile("image", new byte[0]);
        String token = "Bearer token";

        ResponseEntity<String> response = imagesController.uploadImage(file, token);

        assertEquals(ResponseEntity.badRequest().body("Brak zdjęcia."), response);
    }

    @Test
    public void uploadImageReturnsOkWhenFileIsUploadedSuccessfully() throws Exception {
        byte[] fileContent = "fileContent".getBytes();
        MultipartFile file = new MockMultipartFile("image", "originalName", "text/plain", fileContent);
        String token = "Bearer token";
        String userId = "1";

        when(jwtUtil.getId(token.replace("Bearer ", ""))).thenReturn(userId);

        ResponseEntity<String> response = imagesController.uploadImage(file, token);

        assertEquals(ResponseEntity.ok("Zapisano zdjęcie: " + file.getOriginalFilename()), response);
    }

    @Test
    public void uploadImageReturnsInternalServerErrorWhenExceptionIsThrown() throws Exception {
        byte[] fileContent = "fileContent".getBytes();
        MultipartFile file = new MockMultipartFile("image", "originalName", "text/plain", fileContent);
        String token = "Bearer invalidToken";

        when(jwtUtil.getId(token.replace("Bearer ", ""))).thenThrow(new IllegalArgumentException("Invalid token."));

        ResponseEntity<String> response = imagesController.uploadImage(file, token);

        assertEquals(ResponseEntity.internalServerError().body("Błąd: Invalid token."), response);
    }

}