package pl.backend.classifiedImages;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import pl.backend.jwt.JWTUtil;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/classifiedImages")
public class ClassifiedImagesController {

    private final JWTUtil authenticationService;
    private final ClassifiedImagesService classifiedImagesService;

    public ClassifiedImagesController(JWTUtil authenticationService, ClassifiedImagesService classifiedImagesService) {
        this.authenticationService = authenticationService;
        this.classifiedImagesService = classifiedImagesService;
    }

    @PostMapping("/upload")
    public ResponseEntity<String> uploadImage(@RequestParam("image") MultipartFile file, @RequestParam("classifiedText") String classifiedText, @RequestParam("userText") String userText, @RequestHeader("Authorization") String token) {
//      DEBUG SECTION--------------
        System.out.println("File: " + file);
        System.out.println("Classified text: " + classifiedText);
        System.out.println("User txt: " + userText);
        System.out.println("Token: " + token);
//      ---------------------------
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

            ClassifiedImagesUser userImage = new ClassifiedImagesUser();
            userImage.setUserId(userId);
            userImage.setImageName(fileName);
            userImage.setImageData(bytes);
            userImage.setClassifiedText(classifiedText);
            userImage.setUserText(userText);

            classifiedImagesService.saveImage(userImage);

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

        List<ClassifiedImagesUser> images = classifiedImagesService.getAllImagesForUser(userId);
        if (images.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Nie znaleziono zdjęć dla użytkownika.");
        }

        List<String> imageNames = images.stream()
                .map(ClassifiedImagesUser::getImageName)
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
        return classifiedImagesService.getImageData(userId, imageName);
    }
}