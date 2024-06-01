package pl.backend.images;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class ImagesService {
    private final ImagesRepository imagesRepository;

    @Autowired
    public ImagesService(ImagesRepository imagesRepository) {
        this.imagesRepository = imagesRepository;
    }

    @Transactional  // Dodajemy adnotację @Transactional
    public List<ImagesUser> getAllImagesForUser(String userId) {
        return imagesRepository.findByUserId(userId);
    }

    @Transactional
    public ResponseEntity<byte[]> getImageData(String userId, String imageName) {
        ImagesUser imagesUser = imagesRepository.findByUserIdAndImageName(userId, imageName);
        if (imagesUser != null) {
            byte[] imageData = imagesUser.getImageData();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.IMAGE_JPEG);
            headers.setContentLength(imageData.length);
            return new ResponseEntity<>(imageData, headers, HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    @Transactional
    public ImagesUser saveImage(ImagesUser imagesUser) {
        return imagesRepository.save(imagesUser);
    }
}