package com.gr3530904_90104.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Temporal;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import com.gr3530904_90104.table.Offer;

import javax.persistence.TemporalType;
import java.util.Date;
import java.util.List;

@Repository
public interface OfferRepository extends JpaRepository<Offer, Integer> {
    List<Offer> findByCardIdAndDateBetween(Integer cardId,
                                           @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                           @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    List<Offer> findByCardIdAndVendorIdAndDateBetween(Integer cardId,
                                                      Integer vendorId,
                                                      @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                                      @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    List<Offer> findByCardIdAndShopIdAndDateBetween(Integer cardId,
                                                    Integer shopId,
                                                    @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                                    @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    Page<Offer> findByShopIdOrderByCardPopularityAsc(Integer shopId, Pageable pageable);

    Page<Offer> findByShopIdAndVendorIdOrderByCardPopularityAsc(Integer shopId, Integer vendorId, Pageable pageable);
}
