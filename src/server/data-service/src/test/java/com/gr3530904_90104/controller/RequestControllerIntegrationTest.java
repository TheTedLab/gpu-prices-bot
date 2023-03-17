package com.gr3530904_90104.controller;

import com.gr3530904_90104.config.TestConfig;
import com.gr3530904_90104.repository.*;
import io.zonky.test.db.AutoConfigureEmbeddedDatabase;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.util.stream.Stream;

import static com.gr3530904_90104.controller.data.RequestControllerIntegrationTestDataSupplier.*;
import static io.zonky.test.db.AutoConfigureEmbeddedDatabase.RefreshMode.AFTER_EACH_TEST_METHOD;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringRunner.class)
@SpringBootTest
@ActiveProfiles("integrationTest")
@AutoConfigureEmbeddedDatabase(refresh = AFTER_EACH_TEST_METHOD)
@Import(TestConfig.class)
public class RequestControllerIntegrationTest {
    @Autowired
    private ArchitectureRepository architectureRepository;
    @Autowired
    private CardRepository cardRepository;
    @Autowired
    private OfferRepository offerRepository;
    @Autowired
    private ShopRepository shopRepository;
    @Autowired
    private VendorRepository vendorRepository;
    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    @Test
    public void testPutNewDataWithEmptyDataBase() throws Exception {
        String json = testPutNewDataWithEmptyDataBaseJsonData();
        String url = "/insert-new-data";
        mockMvc.perform(
                post(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().is(201));
        Assertions.assertEquals(30, offerRepository.findAll().size());
        Assertions.assertEquals(2, architectureRepository.findAll().size());
        Assertions.assertEquals(30, cardRepository.findAll().size());
        Assertions.assertEquals(6, vendorRepository.findAll().size());
        Assertions.assertEquals(3, shopRepository.findAll().size());
    }

    @Test
    public void testPutNewDataWithNotEmptyDataBase() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String json = testPutNewDataWithNotEmptyDataBaseJsonData();
        String url = "/insert-new-data";
        mockMvc.perform(
                post(url)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andExpect(status().is(201));
        Assertions.assertEquals(60, offerRepository.findAll().size());
        Assertions.assertEquals(2, architectureRepository.findAll().size());
        Assertions.assertEquals(36, cardRepository.findAll().size());
        Assertions.assertEquals(7, vendorRepository.findAll().size());
        Assertions.assertEquals(3, shopRepository.findAll().size());
    }

    @Test
    public void testPutNewDataWithWrongRequestBody() throws Exception {
        String url = "/insert-new-data";
        mockMvc.perform(
                        post(url)
                                .contentType(MediaType.APPLICATION_JSON)
                                .content("json{}"))
                .andExpect(status().is4xxClientError());
    }

    @Test
    public void testIsCardPresentPositive() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/is-card-present?cardName=GEFORCE RTX 4080 EAGLE OC 16GB";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals("true", result.getResponse().getContentAsString());
    }

    @Test
    public void testIsCardPresentNegative() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/is-card-present?cardName=GEFORCE RTX 1060 3GB";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("false", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForCardFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/price?cardName=GEFORCE RTX 4080 EAGLE OC 16GB";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals(testGetPriceForCardFoundExpectedData(), result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForCardNotFoundDate() throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/price?cardName=GEFORCE RTX 4080 EAGLE OC 16GB";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForCardNotFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/price?cardName=GEFORCE RTX 1060 3GB";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForVendorFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/price/for-vendor?vendorName=GIGABYTE&seriesName=GEFORCE RTX 4080";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals(testGetPriceForVendorFoundExpectedData(), result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForVendorNotFoundDate() throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/price/for-vendor?vendorName=GIGABYTE&seriesName=GEFORCE RTX 4080";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForVendorNotFoundSource")
    public void testGetPriceForVendorNotFound(String vendor, String series) throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/price/for-vendor?vendorName=" + vendor + "&seriesName=" + series;
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForShopFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/price/for-shop?shopName=MVIDEO&seriesName=GEFORCE RTX 4080";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals(testGetPriceForShopFoundExpectedData(), result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPriceForShopNotFoundDate() throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/price/for-shop?shopName=MVIDEO&seriesName=GEFORCE RTX 4080";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @ParameterizedTest
    @MethodSource("testGetPriceForShopNotFoundSource")
    public void testGetPriceForShopNotFound(String shop, String series) throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/price/for-shop?shopName=" + shop + "&seriesName=" + series;
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForShopFound() throws Exception {
        prepareDateBase(popularityDataBasePrepareData());
        String url = "/popularity/for-shop?shopName=MVIDEO";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals(testGetPopularityForShopFoundExpectedData(), result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForShopNotFoundDate() throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/popularity/for-shop?shopName=MVIDEO";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForShopNotFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/popularity/for-shop?shopName=ELDORADO";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("[]", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForVendorFound() throws Exception {
        prepareDateBase(popularityDataBasePrepareData());
        String url = "/popularity/for-vendor?vendorName=MSI";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().isOk())
                .andReturn();
        Assertions.assertEquals(testGetPopularityForVendorFoundExpectedData(), result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForVendorNotFoundDate() throws Exception {
        prepareDateBase(defaultDataBasePrepareOldData());
        String url = "/popularity/for-vendor?vendorName=MSI";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("{}", result.getResponse().getContentAsString());
    }

    @Test
    public void testGetPopularityForVendorNotFound() throws Exception {
        prepareDateBase(defaultDataBasePrepareData());
        String url = "/popularity/for-vendor?vendorName=ASUS";
        MvcResult result = mockMvc.perform(
                        get(url))
                .andExpect(status().is(404))
                .andReturn();
        Assertions.assertEquals("{}", result.getResponse().getContentAsString());
    }

    public static Stream<Arguments> testGetPriceForVendorNotFoundSource() {
        return Stream.of(
                Arguments.of("PNY", "GEFORCE RTX 3070 TI"),
                Arguments.of("PNY", "GEFORCE RTX 1060"),
                Arguments.of("GIGABYTE", "GEFORCE RTX 1060")
        );
    }

    public static Stream<Arguments> testGetPriceForShopNotFoundSource() {
        return Stream.of(
                Arguments.of("ELDORADO", "GEFORCE RTX 3070 TI"),
                Arguments.of("ELDORADO", "GEFORCE RTX 1060"),
                Arguments.of("MVIDEO", "GEFORCE RTX 1060")
        );
    }

    private void prepareDateBase(String sqlQuery) {
        namedParameterJdbcTemplate.update(sqlQuery, new MapSqlParameterSource());
    }
}
