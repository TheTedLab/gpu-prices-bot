package com.gr3530904_90104.repository;

import com.gr3530904_90104.table.Offer;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Temporal;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import javax.persistence.TemporalType;
import java.util.Date;
import java.util.List;

@Repository
public interface OfferRepository extends JpaRepository<Offer, Integer> {
    List<Offer> findByCardIdAndDateBetween(@Param("cardId") Integer cardId,
                                           @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                           @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    List<Offer> findByCardIdAndVendorIdAndDateBetween(@Param("cardIds") List<Integer> cardIds,
                                                      @Param("vendorId") Integer vendorId,
                                                      @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                                      @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    List<Offer> findByCardIdAndShopIdAndDateBetween(@Param("cardIds") List<Integer> cardIds,
                                                    @Param("shopId") Integer shopId,
                                                    @Temporal(TemporalType.DATE) @Param("startDate") Date startDate,
                                                    @Temporal(TemporalType.DATE) @Param("endDate") Date endDate);

    Page<Offer> findByShopIdAndDateOrderByCardPopularityAsc(Integer shopId, Date date, Pageable pageable);

    Page<Offer> findByShopIdAndVendorIdAndDateOrderByCardPopularityAsc(Integer shopId, Integer vendorId, Date date, Pageable pageable);
}
