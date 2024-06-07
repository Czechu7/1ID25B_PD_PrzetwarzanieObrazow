package pl.backend.images;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.validation.annotation.Validated;

@Getter
@Setter
@NoArgsConstructor
@Validated
@Entity
@Table(name = "user_images")
public class ImagesUser {
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "user_id", nullable = false)
    private String userId;

    @Column(name = "image_name", nullable = false)
    private String imageName;

    @Lob
    @Basic(fetch = FetchType.LAZY)
    @Column(name = "image_data", nullable = false)
    private byte[] imageData;

    public ImagesUser(String userId, String imageName, byte[] imageData) {
        this.userId = userId;
        this.imageName = imageName;
        this.imageData = imageData;
    }
}