package pl.backend.images;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.*;

import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import pl.backend.jwt.JWTUtil;


@RestController
@RequestMapping("/images")
public class ImagesController {

    @Value("${images.target-path}")
    private String TARGET_FOLDER;
    private final JWTUtil authenticationService;

    public ImagesController(JWTUtil authenticationService) {
        this.authenticationService = authenticationService;
    }

    public void setTargetFolder(String targetFolder) {
        this.TARGET_FOLDER = targetFolder;
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
        String fileName = new File(file.getOriginalFilename()).getName();

        Path userDirectory = Paths.get(TARGET_FOLDER, userId);
        if (!Files.exists(userDirectory)) {
            Files.createDirectories(userDirectory);
        }
        Path filePath = userDirectory.resolve(fileName);
        Files.write(filePath, bytes);

        return ResponseEntity.ok("Zapisano zdjęcie: " + file.getOriginalFilename());
    } catch (Exception e) {
        e.printStackTrace();
        return ResponseEntity.internalServerError().body("Błąd: " + e.getMessage());
    }
}

}

