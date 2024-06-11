package pl.backend.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import jakarta.annotation.security.PermitAll;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;


@Controller
public class PhotoAnnotationController {

    private static final Logger logger = LoggerFactory.getLogger(PhotoAnnotationController.class);

    @MessageMapping("/annotate/{photoId}")
    @SendTo("/topic/{photoId}")
    public AnnotationMessage handleAnnotation(@DestinationVariable String photoId, AnnotationMessage message) {
        logger.info("Received annotation for photoId: {}", photoId);
        logger.info("Annotation message: {}", message);
        return message;
    }
}


