package pl.backend.classifiedImages;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
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

    // W pliku ClassifiedImagesService.java
    @Transactional
    public List<Map<String, Object>> getUserClassifiedTexts(String userId) {
        List<ClassifiedImagesUser> userImages = classifiedImagesRepository.findByUserId(userId);

        List<Map<String, Object>> classifications = userImages.stream()
                .map(ClassifiedImagesUser::getClassifiedText)
                .map(text -> text.split("\n"))
                .flatMap(Arrays::stream)
                .map(line -> {
                    String[] parts = line.split(": ");
                    String classification = parts[0];
                    double percentage = Double.parseDouble(parts[1].replace("%", ""));
                    Map<String, Object> map = new HashMap<>();
                    map.put("classification", classification);
                    map.put("percentage", percentage);
                    return map;
                })
                .collect(Collectors.toList());

        return classifications;
    }

    @Transactional
    public Map<String, Double> getUserClassificationStats(String userId) {
        // Pobierz wszystkie obrazy dla użytkownika
        List<ClassifiedImagesUser> userImages = classifiedImagesRepository.findByUserId(userId);

        // Pobierz tekst klasyfikacji dla każdego obrazu
        List<Map<String, Object>> classifications = getUserClassifiedTexts(userId);

        // Oblicz sumę wszystkich procentów
        double totalPercentage = classifications.stream()
                .mapToDouble(c -> (Double) c.get("percentage"))
                .sum();

        // Zlicz wystąpienia każdej klasyfikacji i oblicz jej procent jako procent sumy wszystkich procentów
        Map<String, Double> classificationCounts = classifications.stream()
                .collect(Collectors.toMap(
                        c -> c.get("classification").toString(),
                        c -> ((Double) c.get("percentage")) / totalPercentage * 100,
                        Double::sum));

        // Zaokrąglij procenty do najbliższej liczby całkowitej i oblicz ich sumę
        Map<String, Long> roundedCounts = classificationCounts.entrySet().stream()
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        e -> Math.round(e.getValue())));

        long sum = roundedCounts.values().stream().mapToLong(Long::longValue).sum();

        // Jeżeli suma zaokrąglonych procentów jest różna od 100, skoryguj największy procent
        if (sum != 100) {
            String maxKey = Collections.max(roundedCounts.entrySet(), Map.Entry.comparingByValue()).getKey();
            roundedCounts.put(maxKey, roundedCounts.get(maxKey) + 100 - sum);
        }

        // Zwróć zaokrąglone procenty
        return roundedCounts.entrySet().stream()
                .collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().doubleValue()));
    }
}