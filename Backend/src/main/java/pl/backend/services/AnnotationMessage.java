package pl.backend.services;

public class AnnotationMessage {
    private String photoId;
    private String userId;
    private String content;

    public AnnotationMessage() {
    }

    public AnnotationMessage(String photoId, String userId, String content) {
        this.photoId = photoId;
        this.userId = userId;
        this.content = content;
    }

    public String getPhotoId() {
        return photoId;
    }

    public void setPhotoId(String photoId) {
        this.photoId = photoId;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}
