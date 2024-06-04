package pl.backend.classifiedImages;

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
@Table(name = "classified_user_images")
public class ClassifiedImagesUser {
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

    @Column(name = "classified_text", nullable = false)
    private String classifiedText;

    @Column(name = "user_text", nullable = false)
    private String userText;

    public ClassifiedImagesUser(String userId, String imageName, byte[] imageData, String classifiedText, String userText) {
        this.userId = userId;
        this.imageName = imageName;
        this.imageData = imageData;
        this.classifiedText = classifiedText;
        this.userText = userText;
    }
}