package pl.backend.classifiedImages;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ClassifiedImagesService {
    private final ClassifiedImagesRepository classifiedImagesRepository;

    @Autowired
    public ClassifiedImagesService(ClassifiedImagesRepository classifiedImagesRepository) {
        this.classifiedImagesRepository = classifiedImagesRepository;
    }

    @Transactional
    public List<ClassifiedImagesUser> getAllImagesForUser(String userId) {
        return classifiedImagesRepository.findByUserId(userId);
    }

    @Transactional
    public ResponseEntity<byte[]> getImageData(String userId, String imageName) {
        ClassifiedImagesUser classifiedImagesUser = classifiedImagesRepository.findByUserIdAndImageName(userId, imageName);
        if (classifiedImagesUser != null) {
            byte[] imageData = classifiedImagesUser.getImageData();
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.IMAGE_JPEG);
            headers.setContentLength(imageData.length);
            return new ResponseEntity<>(imageData, headers, HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    @Transactional
    public ClassifiedImagesUser saveImage(ClassifiedImagesUser classifiedImagesUser) {
        return classifiedImagesRepository.save(classifiedImagesUser);
    }

    public Map<String, Double> getClassifiedTextStatistics() {
        List<ClassifiedImagesUser> allImages = classifiedImagesRepository.findAll();

        if (allImages.isEmpty()) {
            return Collections.emptyMap();
        }

        Map<String, Long> classifiedTextCount = allImages.stream()
                .collect(Collectors.groupingBy(ClassifiedImagesUser::getClassifiedText, Collectors.counting()));

        long totalTexts = allImages.size();

        Map<String, Double> classifiedTextPercentage = new HashMap<>();
        for (Map.Entry<String, Long> entry : classifiedTextCount.entrySet()) {
            double percentage = 100.0 * entry.getValue() / totalTexts;
            classifiedTextPercentage.put(entry.getKey(), percentage);
        }

        return classifiedTextPercentage;
    }
}