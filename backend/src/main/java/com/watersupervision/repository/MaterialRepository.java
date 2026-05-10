package com.watersupervision.repository;

import com.watersupervision.entity.Material;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface MaterialRepository extends JpaRepository<Material, Long> {
    List<Material> findByApplicantIdOrderByCreatedAtDesc(Long applicantId);
    List<Material> findByStatusOrderByCreatedAtDesc(Material.MaterialStatus status);
}
