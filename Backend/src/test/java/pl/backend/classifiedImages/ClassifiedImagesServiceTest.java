package pl.backend.classifiedImages;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class ClassifiedImagesServiceTest {

    @Mock
    private ClassifiedImagesRepository classifiedImagesRepository;

    @InjectMocks
    private ClassifiedImagesService classifiedImagesService;

    @Test
    public void returnsImagesForUser() {
        String userId = "user1";
        ClassifiedImagesUser classifiedImagesUser = new ClassifiedImagesUser();
        List<ClassifiedImagesUser> expectedImages = Collections.singletonList(classifiedImagesUser);

        when(classifiedImagesRepository.findByUserId(userId)).thenReturn(expectedImages);

        List<ClassifiedImagesUser> actualImages = classifiedImagesService.getAllImagesForUser(userId);

        assertEquals(expectedImages, actualImages);
    }

    @Test
    public void returnsImageData() {
        String userId = "user1";
        String imageName = "image1";
        ClassifiedImagesUser classifiedImagesUser = new ClassifiedImagesUser();
        classifiedImagesUser.setImageData(new byte[]{1, 2, 3});

        when(classifiedImagesRepository.findByUserIdAndImageName(userId, imageName)).thenReturn(classifiedImagesUser);

        ResponseEntity<byte[]> response = classifiedImagesService.getImageData(userId, imageName);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(classifiedImagesUser.getImageData(), response.getBody());
    }

    @Test
    public void returnsNotFoundWhenImageDoesNotExist() {
        String userId = "user1";
        String imageName = "image1";

        when(classifiedImagesRepository.findByUserIdAndImageName(userId, imageName)).thenReturn(null);

        ResponseEntity<byte[]> response = classifiedImagesService.getImageData(userId, imageName);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    public void returnsSavedImage() {
        ClassifiedImagesUser classifiedImagesUser = new ClassifiedImagesUser();

        when(classifiedImagesRepository.save(classifiedImagesUser)).thenReturn(classifiedImagesUser);

        ClassifiedImagesUser savedImage = classifiedImagesService.saveImage(classifiedImagesUser);

        assertEquals(classifiedImagesUser, savedImage);
    }
}