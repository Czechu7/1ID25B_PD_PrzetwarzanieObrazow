package pl.backend.images;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ImagesRepository extends JpaRepository<ImagesUser, Long> {
    List<ImagesUser> findByUserId(String userId);
    ImagesUser findByUserIdAndImageName(String userId, String imageName);
}