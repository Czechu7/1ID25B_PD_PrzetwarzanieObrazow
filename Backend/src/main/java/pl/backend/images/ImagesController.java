package pl.backend.images;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import pl.backend.images.ImagesRepository;
import pl.backend.images.ImagesService;
import pl.backend.jwt.JWTUtil;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/images")
public class ImagesController {

    private final JWTUtil authenticationService;
    private final ImagesService imagesService;

    public ImagesController(JWTUtil authenticationService, ImagesService imagesService) {
        this.authenticationService = authenticationService;
        this.imagesService = imagesService;
    }

    @PostMapping("/upload")
    public ResponseEntity<String> uploadImage(@RequestParam("image") MultipartFile file, @RequestHeader("Authorization") String token) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("Brak zdjęcia.");
        }
        try {
            token = token.replace("Bearer ", "");
            var userId = this.authenticationService.getId(token);
            byte[] bytes = file.getBytes();
            if (bytes.length == 0) {
                return ResponseEntity.badRequest().body("Plik jest pusty.");
            }
            String fileName = new File(Objects.requireNonNull(file.getOriginalFilename())).getName();

            ImagesUser userImage = new ImagesUser();
            userImage.setUserId(userId);
            userImage.setImageName(fileName);
            userImage.setImageData(bytes);

            imagesService.saveImage(userImage);

            return ResponseEntity.status(HttpStatus.CREATED).body("Zdjęcie zostało przesłane.");
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Błąd przy przesyłaniu zdjęcia.");
        }
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<?> getAllImagesForUser(@PathVariable String userId, @RequestHeader("Authorization") String token) {
        token = token.replace("Bearer ", "");
        String authUserId = this.authenticationService.getId(token);
        if (!authUserId.equals(userId)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Nieautoryzowany dostęp.");
        }

        List<ImagesUser> images = imagesService.getAllImagesForUser(userId);
        if (images.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Nie znaleziono zdjęć dla użytkownika.");
        }

        List<String> imageNames = images.stream()
                .map(ImagesUser::getImageName)
                .collect(Collectors.toList());

        return ResponseEntity.ok(imageNames);
    }

    @GetMapping("/user/{userId}/image/{imageName}")
    public ResponseEntity<byte[]> getImageForUser(@PathVariable String userId, @PathVariable String imageName, @RequestHeader("Authorization") String token) {
        token = token.replace("Bearer ", "");
        String authUserId = this.authenticationService.getId(token);
        if (!authUserId.equals(userId)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(null);
        }

        return imagesService.getImageData(userId, imageName);
    }
}
