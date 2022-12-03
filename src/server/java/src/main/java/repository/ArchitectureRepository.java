package repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import table.Architecture;

import java.util.Optional;

@Repository
public interface ArchitectureRepository extends JpaRepository<Architecture, Integer> {
    public Optional<Architecture> findArchitectureById(Integer id);
    public Optional<Architecture> findArchitectureByName(String name);
}
