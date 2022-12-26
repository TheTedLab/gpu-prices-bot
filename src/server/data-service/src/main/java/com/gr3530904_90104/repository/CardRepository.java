package com.gr3530904_90104.repository;

import com.gr3530904_90104.table.Card;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CardRepository extends JpaRepository<Card, Integer> {
    Optional<Card> findCardById(Integer id);
    Optional<Card> findCardByName(String name);
    List<Card> findCardsByCardSeries(String cardSeries);
}
