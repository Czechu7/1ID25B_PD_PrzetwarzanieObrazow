package pl.backend.classifiedImages;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ClassifiedImagesRepository extends JpaRepository<ClassifiedImagesUser, Long> {
    List<ClassifiedImagesUser> findByUserId(String userId);
    ClassifiedImagesUser findByUserIdAndImageName(String userId, String imageName);
}