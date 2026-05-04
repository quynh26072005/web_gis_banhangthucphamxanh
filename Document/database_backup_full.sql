--
-- PostgreSQL database dump
--

\restrict TQbfbp5hV7RE6rUAnTn64PflKaMYNVeNcUxYh8ymFne2X2tLoLcQdAlRsVjmJvM

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.food_store_storeadmin DROP CONSTRAINT IF EXISTS food_store_storeadmin_user_id_b28a5e37_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.food_store_storeadmin DROP CONSTRAINT IF EXISTS food_store_storeadmin_farm_id_572ebddc_fk_food_store_farm_id;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktran_supplier_id_a133701a_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktran_product_id_84ea055e_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktran_order_id_64bb83c3_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktran_farm_id_493f6ff1_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktran_created_by_id_43dbae19_fk_auth_user;
ALTER TABLE IF EXISTS ONLY public.food_store_stockalert DROP CONSTRAINT IF EXISTS food_store_stockalert_resolved_by_id_a9ae68ac_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.food_store_stockalert DROP CONSTRAINT IF EXISTS food_store_stockalert_farm_id_e6249491_fk_food_store_farm_id;
ALTER TABLE IF EXISTS ONLY public.food_store_stockalert DROP CONSTRAINT IF EXISTS food_store_stockaler_product_id_b4244a82_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_shipper DROP CONSTRAINT IF EXISTS food_store_shipper_user_id_72a33852_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.food_store_shipper DROP CONSTRAINT IF EXISTS food_store_shipper_assigned_farm_id_b497bb82_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_product DROP CONSTRAINT IF EXISTS food_store_product_farm_id_df30caee_fk_food_store_farm_id;
ALTER TABLE IF EXISTS ONLY public.food_store_product DROP CONSTRAINT IF EXISTS food_store_product_category_id_163e3ba4_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_passwordreset DROP CONSTRAINT IF EXISTS food_store_passwordreset_user_id_a7819a53_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.food_store_orderitem DROP CONSTRAINT IF EXISTS food_store_orderitem_product_id_43e845e6_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_orderitem DROP CONSTRAINT IF EXISTS food_store_orderitem_order_id_5be5ed12_fk_food_store_order_id;
ALTER TABLE IF EXISTS ONLY public.food_store_order DROP CONSTRAINT IF EXISTS food_store_order_delivery_zone_id_1a3f1f54_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_order DROP CONSTRAINT IF EXISTS food_store_order_customer_id_437a55ee_fk_food_store_customer_id;
ALTER TABLE IF EXISTS ONLY public.food_store_order DROP CONSTRAINT IF EXISTS food_store_order_assigned_shipper_id_b7958c26_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_order DROP CONSTRAINT IF EXISTS food_store_order_assigned_farm_id_9f7bbc41_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_inventoryreport DROP CONSTRAINT IF EXISTS food_store_inventory_farm_id_aaed62d8_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_inventoryreport DROP CONSTRAINT IF EXISTS food_store_inventory_created_by_id_788205b9_fk_auth_user;
ALTER TABLE IF EXISTS ONLY public.food_store_customer DROP CONSTRAINT IF EXISTS food_store_customer_user_id_6fe6a5ae_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.food_store_cartitem DROP CONSTRAINT IF EXISTS food_store_cartitem_product_id_8d7bed26_fk_food_stor;
ALTER TABLE IF EXISTS ONLY public.food_store_cartitem DROP CONSTRAINT IF EXISTS food_store_cartitem_cart_id_4bc929e4_fk_food_store_cart_id;
ALTER TABLE IF EXISTS ONLY public.food_store_cart DROP CONSTRAINT IF EXISTS food_store_cart_customer_id_22389329_fk_food_store_customer_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.food_store_storeadmin_farm_id_572ebddc;
DROP INDEX IF EXISTS public.food_store_stocktransaction_supplier_id_a133701a;
DROP INDEX IF EXISTS public.food_store_stocktransaction_product_id_84ea055e;
DROP INDEX IF EXISTS public.food_store_stocktransaction_order_id_64bb83c3;
DROP INDEX IF EXISTS public.food_store_stocktransaction_farm_id_493f6ff1;
DROP INDEX IF EXISTS public.food_store_stocktransaction_created_by_id_43dbae19;
DROP INDEX IF EXISTS public.food_store_stockalert_resolved_by_id_a9ae68ac;
DROP INDEX IF EXISTS public.food_store_stockalert_product_id_b4244a82;
DROP INDEX IF EXISTS public.food_store_stockalert_farm_id_e6249491;
DROP INDEX IF EXISTS public.food_store_shipper_assigned_farm_id_b497bb82;
DROP INDEX IF EXISTS public.food_store_product_farm_id_df30caee;
DROP INDEX IF EXISTS public.food_store_product_category_id_163e3ba4;
DROP INDEX IF EXISTS public.food_store_passwordreset_user_id_a7819a53;
DROP INDEX IF EXISTS public.food_store_orderitem_product_id_43e845e6;
DROP INDEX IF EXISTS public.food_store_orderitem_order_id_5be5ed12;
DROP INDEX IF EXISTS public.food_store_order_delivery_zone_id_1a3f1f54;
DROP INDEX IF EXISTS public.food_store_order_customer_id_437a55ee;
DROP INDEX IF EXISTS public.food_store_order_assigned_shipper_id_b7958c26;
DROP INDEX IF EXISTS public.food_store_order_assigned_farm_id_9f7bbc41;
DROP INDEX IF EXISTS public.food_store_inventoryreport_farm_id_aaed62d8;
DROP INDEX IF EXISTS public.food_store_inventoryreport_created_by_id_788205b9;
DROP INDEX IF EXISTS public.food_store_cartitem_product_id_8d7bed26;
DROP INDEX IF EXISTS public.food_store_cartitem_cart_id_4bc929e4;
DROP INDEX IF EXISTS public.food_store__product_bee5b6_idx;
DROP INDEX IF EXISTS public.food_store__farm_id_057a7e_idx;
DROP INDEX IF EXISTS public.food_store__created_318c1b_idx;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.food_store_supplier DROP CONSTRAINT IF EXISTS food_store_supplier_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_storeadmin DROP CONSTRAINT IF EXISTS food_store_storeadmin_user_id_key;
ALTER TABLE IF EXISTS ONLY public.food_store_storeadmin DROP CONSTRAINT IF EXISTS food_store_storeadmin_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_stocktransaction DROP CONSTRAINT IF EXISTS food_store_stocktransaction_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_stockalert DROP CONSTRAINT IF EXISTS food_store_stockalert_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_shipper DROP CONSTRAINT IF EXISTS food_store_shipper_user_id_key;
ALTER TABLE IF EXISTS ONLY public.food_store_shipper DROP CONSTRAINT IF EXISTS food_store_shipper_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_product DROP CONSTRAINT IF EXISTS food_store_product_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_passwordreset DROP CONSTRAINT IF EXISTS food_store_passwordreset_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_orderitem DROP CONSTRAINT IF EXISTS food_store_orderitem_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_order DROP CONSTRAINT IF EXISTS food_store_order_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_inventoryreport DROP CONSTRAINT IF EXISTS food_store_inventoryreport_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_farm DROP CONSTRAINT IF EXISTS food_store_farm_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_emailverification DROP CONSTRAINT IF EXISTS food_store_emailverification_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_deliveryzone DROP CONSTRAINT IF EXISTS food_store_deliveryzone_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_customer DROP CONSTRAINT IF EXISTS food_store_customer_user_id_key;
ALTER TABLE IF EXISTS ONLY public.food_store_customer DROP CONSTRAINT IF EXISTS food_store_customer_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_category DROP CONSTRAINT IF EXISTS food_store_category_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_cartitem DROP CONSTRAINT IF EXISTS food_store_cartitem_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_cartitem DROP CONSTRAINT IF EXISTS food_store_cartitem_cart_id_product_id_dfb8b76d_uniq;
ALTER TABLE IF EXISTS ONLY public.food_store_cart DROP CONSTRAINT IF EXISTS food_store_cart_pkey;
ALTER TABLE IF EXISTS ONLY public.food_store_cart DROP CONSTRAINT IF EXISTS food_store_cart_customer_id_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
DROP TABLE IF EXISTS public.food_store_supplier;
DROP TABLE IF EXISTS public.food_store_storeadmin;
DROP TABLE IF EXISTS public.food_store_stocktransaction;
DROP TABLE IF EXISTS public.food_store_stockalert;
DROP TABLE IF EXISTS public.food_store_shipper;
DROP TABLE IF EXISTS public.food_store_product;
DROP TABLE IF EXISTS public.food_store_passwordreset;
DROP TABLE IF EXISTS public.food_store_orderitem;
DROP TABLE IF EXISTS public.food_store_order;
DROP TABLE IF EXISTS public.food_store_inventoryreport;
DROP TABLE IF EXISTS public.food_store_farm;
DROP TABLE IF EXISTS public.food_store_emailverification;
DROP TABLE IF EXISTS public.food_store_deliveryzone;
DROP TABLE IF EXISTS public.food_store_customer;
DROP TABLE IF EXISTS public.food_store_category;
DROP TABLE IF EXISTS public.food_store_cartitem;
DROP TABLE IF EXISTS public.food_store_cart;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: food_store_cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_cart (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    customer_id bigint NOT NULL
);


ALTER TABLE public.food_store_cart OWNER TO postgres;

--
-- Name: food_store_cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_cart ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_cart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_cartitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_cartitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    added_at timestamp with time zone NOT NULL,
    cart_id bigint NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT food_store_cartitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.food_store_cartitem OWNER TO postgres;

--
-- Name: food_store_cartitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_cartitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_cartitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_category (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    image character varying(100) NOT NULL
);


ALTER TABLE public.food_store_category OWNER TO postgres;

--
-- Name: food_store_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_category ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_customer (
    id bigint NOT NULL,
    phone character varying(20) NOT NULL,
    address text NOT NULL,
    latitude double precision,
    longitude double precision,
    created_at timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.food_store_customer OWNER TO postgres;

--
-- Name: food_store_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_customer ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_deliveryzone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_deliveryzone (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    area_description text NOT NULL,
    delivery_fee numeric(8,2) NOT NULL,
    delivery_time character varying(50) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.food_store_deliveryzone OWNER TO postgres;

--
-- Name: food_store_deliveryzone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_deliveryzone ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_deliveryzone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_emailverification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_emailverification (
    id bigint NOT NULL,
    email character varying(254) NOT NULL,
    otp_code character varying(6) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    is_verified boolean NOT NULL,
    attempts integer NOT NULL,
    username character varying(150) NOT NULL,
    password character varying(255) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    phone character varying(20) NOT NULL
);


ALTER TABLE public.food_store_emailverification OWNER TO postgres;

--
-- Name: food_store_emailverification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_emailverification ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_emailverification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_farm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_farm (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    address text NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    description text NOT NULL,
    latitude double precision,
    longitude double precision,
    organic_certified boolean NOT NULL,
    certification_number character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.food_store_farm OWNER TO postgres;

--
-- Name: food_store_farm_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_farm ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_farm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_inventoryreport; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_inventoryreport (
    id bigint NOT NULL,
    report_date date NOT NULL,
    total_products integer NOT NULL,
    total_quantity integer NOT NULL,
    total_value numeric(15,2) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by_id integer,
    farm_id bigint NOT NULL
);


ALTER TABLE public.food_store_inventoryreport OWNER TO postgres;

--
-- Name: food_store_inventoryreport_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_inventoryreport ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_inventoryreport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_order (
    id bigint NOT NULL,
    status character varying(20) NOT NULL,
    delivery_address text NOT NULL,
    delivery_latitude double precision,
    delivery_longitude double precision,
    delivery_fee numeric(8,2) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    delivered_at timestamp with time zone,
    notes text NOT NULL,
    customer_id bigint NOT NULL,
    delivery_zone_id bigint,
    assigned_farm_id bigint,
    delivery_distance_km double precision,
    delivery_duration_min double precision,
    payment_method character varying(20) NOT NULL,
    payment_reference character varying(100) NOT NULL,
    payment_amount numeric(12,2),
    payment_date timestamp with time zone,
    payment_status character varying(20) NOT NULL,
    proof_image character varying(100),
    shipper_accepted_at timestamp with time zone,
    shipper_notes text NOT NULL,
    shipper_picked_at timestamp with time zone,
    assigned_shipper_id bigint
);


ALTER TABLE public.food_store_order OWNER TO postgres;

--
-- Name: food_store_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_order ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_orderitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_orderitem (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    price numeric(10,2) NOT NULL,
    order_id bigint NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT food_store_orderitem_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.food_store_orderitem OWNER TO postgres;

--
-- Name: food_store_orderitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_orderitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_orderitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_passwordreset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_passwordreset (
    id bigint NOT NULL,
    email character varying(254) NOT NULL,
    otp_code character varying(6) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    is_used boolean NOT NULL,
    attempts integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.food_store_passwordreset OWNER TO postgres;

--
-- Name: food_store_passwordreset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_passwordreset ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_passwordreset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_product (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    description text NOT NULL,
    price numeric(10,2) NOT NULL,
    unit character varying(20) NOT NULL,
    image character varying(100) NOT NULL,
    stock_quantity integer NOT NULL,
    is_available boolean NOT NULL,
    nutritional_info text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    category_id bigint NOT NULL,
    farm_id bigint NOT NULL,
    CONSTRAINT food_store_product_stock_quantity_check CHECK ((stock_quantity >= 0))
);


ALTER TABLE public.food_store_product OWNER TO postgres;

--
-- Name: food_store_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_shipper; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_shipper (
    id bigint NOT NULL,
    phone character varying(20) NOT NULL,
    vehicle_number character varying(50) NOT NULL,
    status character varying(20) NOT NULL,
    total_deliveries integer NOT NULL,
    today_deliveries integer NOT NULL,
    cod_holding numeric(12,2) NOT NULL,
    today_earnings numeric(12,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    assigned_farm_id bigint
);


ALTER TABLE public.food_store_shipper OWNER TO postgres;

--
-- Name: food_store_shipper_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_shipper ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_shipper_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_stockalert; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_stockalert (
    id bigint NOT NULL,
    alert_type character varying(20) NOT NULL,
    threshold integer NOT NULL,
    current_stock integer NOT NULL,
    is_resolved boolean NOT NULL,
    resolved_at timestamp with time zone,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    farm_id bigint NOT NULL,
    product_id bigint NOT NULL,
    resolved_by_id integer
);


ALTER TABLE public.food_store_stockalert OWNER TO postgres;

--
-- Name: food_store_stockalert_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_stockalert ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_stockalert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_stocktransaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_stocktransaction (
    id bigint NOT NULL,
    transaction_type character varying(20) NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2),
    total_amount numeric(12,2),
    stock_before integer NOT NULL,
    stock_after integer NOT NULL,
    reference_number character varying(50) NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by_id integer,
    farm_id bigint NOT NULL,
    order_id bigint,
    product_id bigint NOT NULL,
    supplier_id bigint
);


ALTER TABLE public.food_store_stocktransaction OWNER TO postgres;

--
-- Name: food_store_stocktransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_stocktransaction ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_stocktransaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_storeadmin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_storeadmin (
    id bigint NOT NULL,
    phone character varying(20) NOT NULL,
    can_manage_products boolean NOT NULL,
    can_manage_orders boolean NOT NULL,
    can_manage_inventory boolean NOT NULL,
    can_manage_shippers boolean NOT NULL,
    can_view_reports boolean NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    farm_id bigint NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.food_store_storeadmin OWNER TO postgres;

--
-- Name: food_store_storeadmin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_storeadmin ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_storeadmin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: food_store_supplier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.food_store_supplier (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    contact_person character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    address text NOT NULL,
    tax_code character varying(50) NOT NULL,
    notes text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.food_store_supplier OWNER TO postgres;

--
-- Name: food_store_supplier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.food_store_supplier ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.food_store_supplier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (1, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (2, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (3, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (4, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (5, 'Can add group', 1, 'add_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (6, 'Can change group', 1, 'change_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (7, 'Can delete group', 1, 'delete_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (8, 'Can view group', 1, 'view_group');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (9, 'Can add user', 3, 'add_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (10, 'Can change user', 3, 'change_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (11, 'Can delete user', 3, 'delete_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (12, 'Can view user', 3, 'view_user');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (21, 'Can add Category', 8, 'add_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (22, 'Can change Category', 8, 'change_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (23, 'Can delete Category', 8, 'delete_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (24, 'Can view Category', 8, 'view_category');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (25, 'Can add Khách hàng', 9, 'add_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (26, 'Can change Khách hàng', 9, 'change_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (27, 'Can delete Khách hàng', 9, 'delete_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (28, 'Can view Khách hàng', 9, 'view_customer');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (29, 'Can add Delivery Zone', 10, 'add_deliveryzone');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (30, 'Can change Delivery Zone', 10, 'change_deliveryzone');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (31, 'Can delete Delivery Zone', 10, 'delete_deliveryzone');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (32, 'Can view Delivery Zone', 10, 'view_deliveryzone');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (33, 'Can add Store', 12, 'add_farm');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (34, 'Can change Store', 12, 'change_farm');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (35, 'Can delete Store', 12, 'delete_farm');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (36, 'Can view Store', 12, 'view_farm');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (37, 'Can add Đơn hàng', 14, 'add_order');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (38, 'Can change Đơn hàng', 14, 'change_order');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (39, 'Can delete Đơn hàng', 14, 'delete_order');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (40, 'Can view Đơn hàng', 14, 'view_order');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (41, 'Can add Sản phẩm', 17, 'add_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (42, 'Can change Sản phẩm', 17, 'change_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (43, 'Can delete Sản phẩm', 17, 'delete_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (44, 'Can view Sản phẩm', 17, 'view_product');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (45, 'Can add Order Item', 15, 'add_orderitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (46, 'Can change Order Item', 15, 'change_orderitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (47, 'Can delete Order Item', 15, 'delete_orderitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (48, 'Can view Order Item', 15, 'view_orderitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (49, 'Can add Cart', 6, 'add_cart');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (50, 'Can change Cart', 6, 'change_cart');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (51, 'Can delete Cart', 6, 'delete_cart');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (52, 'Can view Cart', 6, 'view_cart');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (53, 'Can add Cart Item', 7, 'add_cartitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (54, 'Can change Cart Item', 7, 'change_cartitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (55, 'Can delete Cart Item', 7, 'delete_cartitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (56, 'Can view Cart Item', 7, 'view_cartitem');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (57, 'Can add Nhà cung cấp', 22, 'add_supplier');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (58, 'Can change Nhà cung cấp', 22, 'change_supplier');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (59, 'Can delete Nhà cung cấp', 22, 'delete_supplier');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (60, 'Can view Nhà cung cấp', 22, 'view_supplier');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (61, 'Can add Báo cáo kiểm kê', 13, 'add_inventoryreport');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (62, 'Can change Báo cáo kiểm kê', 13, 'change_inventoryreport');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (63, 'Can delete Báo cáo kiểm kê', 13, 'delete_inventoryreport');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (64, 'Can view Báo cáo kiểm kê', 13, 'view_inventoryreport');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (65, 'Can add Cảnh báo tồn kho', 19, 'add_stockalert');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (66, 'Can change Cảnh báo tồn kho', 19, 'change_stockalert');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (67, 'Can delete Cảnh báo tồn kho', 19, 'delete_stockalert');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (68, 'Can view Cảnh báo tồn kho', 19, 'view_stockalert');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (69, 'Can add Giao dịch kho', 20, 'add_stocktransaction');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (70, 'Can change Giao dịch kho', 20, 'change_stocktransaction');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (71, 'Can delete Giao dịch kho', 20, 'delete_stocktransaction');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (72, 'Can view Giao dịch kho', 20, 'view_stocktransaction');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (73, 'Can add Shipper', 18, 'add_shipper');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (74, 'Can change Shipper', 18, 'change_shipper');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (75, 'Can delete Shipper', 18, 'delete_shipper');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (76, 'Can view Shipper', 18, 'view_shipper');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (77, 'Can add Quản lý chi nhánh', 21, 'add_storeadmin');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (78, 'Can change Quản lý chi nhánh', 21, 'change_storeadmin');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (79, 'Can delete Quản lý chi nhánh', 21, 'delete_storeadmin');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (80, 'Can view Quản lý chi nhánh', 21, 'view_storeadmin');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (81, 'Can add Xác thực Email', 11, 'add_emailverification');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (82, 'Can change Xác thực Email', 11, 'change_emailverification');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (83, 'Can delete Xác thực Email', 11, 'delete_emailverification');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (84, 'Can view Xác thực Email', 11, 'view_emailverification');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (85, 'Can add Reset Password', 16, 'add_passwordreset');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (86, 'Can change Reset Password', 16, 'change_passwordreset');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (87, 'Can delete Reset Password', 16, 'delete_passwordreset');
INSERT INTO public.auth_permission (id, name, content_type_id, codename) VALUES (88, 'Can view Reset Password', 16, 'view_passwordreset');


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (2, 'pbkdf2_sha256$1200000$zWgp0khJ5AanGZZYDgOvSc$Wn+ZaWmM5/0L2DFYrgjP2gnQmJ/xdslk+/j3SDxtiYw=', NULL, false, 'customer1', 'Nguyễn', 'Văn A', 'customer1@gmail.com', false, true, '2026-02-18 11:45:40+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (3, 'pbkdf2_sha256$1200000$rnyrBTMmCRQtGIwjdLMFlw$itjv6jgXc1FyaQ8dBF4wtNIZyDtpxtWABBqFcY4csjw=', NULL, false, 'customer2', 'Trần', 'Thị B', 'customer2@gmail.com', false, true, '2026-03-02 16:06:44+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (4, 'pbkdf2_sha256$1200000$dPfuySzGgplgEUBpOzpnxH$mVf1tsfkDT2Dc8XpjSSnwucE2I1jLrLYW6jBxDhUmN0=', NULL, false, 'customer3', 'Lê', 'Văn C', 'customer3@gmail.com', false, true, '2026-03-11 11:10:38+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (1, 'pbkdf2_sha256$1200000$GYJ8pfDMfSTYAxBM8gxERF$48roUr7peIhemEhG8KS/RZ0ndXcHpUOdV9+CJ8LktPo=', '2026-05-04 16:42:36.357646+07', true, 'admin', 'Admin', 'System', 'admin@cleanfood.com', true, true, '2026-02-05 09:00:00+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (5, 'pbkdf2_sha256$1200000$eDbr8hRZI9ta8ReNRofFHz$jOWoFILf3wmG/Y5wzHiUcaDGN1TqUZ7zGnDBXntPPIw=', NULL, false, 'shipper1', 'Phạm', 'Văn D', 'shipper1@cleanfood.com', false, true, '2026-03-13 13:35:28+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (6, 'pbkdf2_sha256$1200000$k5UQzs1zJwtWfxGqZT5qgQ$v1uvlRiIif3ek4Rz5VrGvN6z32j07R+JKDTAaqyy3iQ=', NULL, false, 'shipper2', 'Hoàng', 'Thị E', 'shipper2@cleanfood.com', false, true, '2026-03-10 10:05:43+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (7, 'pbkdf2_sha256$1200000$PGDhnYi4Rul7INEIdb988I$9pS94qPlQB512PIKEjdFTMcfhR/A0ngqYxZt1Mmw59U=', NULL, false, 'shipper3', 'Võ', 'Văn F', 'shipper3@cleanfood.com', false, true, '2026-03-07 18:05:25+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (8, 'pbkdf2_sha256$1200000$4D6OzGSQNImrPDtnTZfnWX$nCV0dqZKfGx5vpfR/dUzR/LUuaqgZo+Cjnn9gKcq68Y=', NULL, false, 'storeadmin1', 'Trương', 'Văn G', 'storeadmin1@cleanfood.com', true, true, '2026-03-06 12:03:45+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (9, 'pbkdf2_sha256$1200000$RQM5k8NsdAr9Rx3v9NYfjY$6zUydJ9s+otBM5zv521qxdqpcKu7kIx9mMIsm476s54=', NULL, false, 'storeadmin2', 'Đặng', 'Thị H', 'storeadmin2@cleanfood.com', true, true, '2026-03-04 10:40:54+07');
INSERT INTO public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (10, 'pbkdf2_sha256$1200000$zlGlnYYmFDQYS9ZGuaJXgn$+lx6UhPtNf24nRFxfV+q6Jc2qj3iJXn5E93XrHSh3Ok=', NULL, false, 'storeadmin3', 'Bùi', 'Văn I', 'storeadmin3@cleanfood.com', true, true, '2026-03-06 10:45:37+07');


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_content_type (id, app_label, model) VALUES (1, 'auth', 'group');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (3, 'auth', 'user');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (5, 'sessions', 'session');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (6, 'food_store', 'cart');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (7, 'food_store', 'cartitem');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (8, 'food_store', 'category');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (9, 'food_store', 'customer');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (10, 'food_store', 'deliveryzone');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (11, 'food_store', 'emailverification');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (12, 'food_store', 'farm');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (13, 'food_store', 'inventoryreport');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (14, 'food_store', 'order');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (15, 'food_store', 'orderitem');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (16, 'food_store', 'passwordreset');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (17, 'food_store', 'product');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (18, 'food_store', 'shipper');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (19, 'food_store', 'stockalert');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (20, 'food_store', 'stocktransaction');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (21, 'food_store', 'storeadmin');
INSERT INTO public.django_content_type (id, app_label, model) VALUES (22, 'food_store', 'supplier');


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2026-05-04 16:30:10.877023+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2026-05-04 16:30:10.89042+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (3, 'auth', '0001_initial', '2026-05-04 16:30:10.985502+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2026-05-04 16:30:10.99822+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (5, 'auth', '0003_alter_user_email_max_length', '2026-05-04 16:30:11.013306+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (6, 'auth', '0004_alter_user_username_opts', '2026-05-04 16:30:11.026641+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (7, 'auth', '0005_alter_user_last_login_null', '2026-05-04 16:30:11.038562+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (8, 'auth', '0006_require_contenttypes_0002', '2026-05-04 16:30:11.040267+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2026-05-04 16:30:11.047413+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (10, 'auth', '0008_alter_user_username_max_length', '2026-05-04 16:30:11.05993+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2026-05-04 16:30:11.067422+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (12, 'auth', '0010_alter_group_name_max_length', '2026-05-04 16:30:11.07604+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (13, 'auth', '0011_update_proxy_permissions', '2026-05-04 16:30:11.082886+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2026-05-04 16:30:11.08922+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (15, 'food_store', '0001_initial', '2026-05-04 16:30:11.227779+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (16, 'food_store', '0002_order_assigned_farm', '2026-05-04 16:30:11.243045+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (17, 'food_store', '0003_order_delivery_distance_km_and_more', '2026-05-04 16:30:11.259036+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (18, 'food_store', '0004_rename_farm_to_store', '2026-05-04 16:30:11.279998+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (19, 'food_store', '0005_alter_cart_options_alter_cartitem_options_and_more', '2026-05-04 16:30:11.57071+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (20, 'food_store', '0006_supplier_inventoryreport_stockalert_stocktransaction', '2026-05-04 16:30:11.656448+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (21, 'food_store', '0007_order_payment_method', '2026-05-04 16:30:11.670016+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (22, 'food_store', '0008_order_payment_reference', '2026-05-04 16:30:11.681565+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (23, 'food_store', '0009_order_payment_amount_order_payment_date_and_more', '2026-05-04 16:30:11.710223+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (24, 'food_store', '0010_alter_customer_options_alter_order_options_and_more', '2026-05-04 16:30:12.021072+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (25, 'food_store', '0011_shipper_order_shipper_fields', '2026-05-04 16:30:12.097414+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (26, 'food_store', '0012_alter_order_status', '2026-05-04 16:30:12.111886+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (27, 'food_store', '0013_remove_order_assigned_shipper_and_more', '2026-05-04 16:30:12.18107+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (28, 'food_store', '0014_order_proof_image_order_shipper_accepted_at_and_more', '2026-05-04 16:30:12.272708+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (29, 'food_store', '0015_shipper_assigned_farm_storeadmin', '2026-05-04 16:30:12.31257+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (30, 'food_store', '0016_emailverification_passwordreset', '2026-05-04 16:30:12.344522+07');
INSERT INTO public.django_migrations (id, app, name, applied) VALUES (31, 'sessions', '0001_initial', '2026-05-04 16:30:12.355034+07');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('0e9xx6l04kmvmavtgaxxipd6f0m3z4sv', '.eJxVjMsOwiAQAP9lz4ZAebZH735Ds-yCVA0kpT0Z_9006UGvM5N5w4z7Vua9p3VeGCZQcPllEemZ6iH4gfXeBLW6rUsURyJO28WtcXpdz_ZvULAXmCCjSkhMwcfoWGM22mIM2eoQlGerncnSUPAexwGJnU_auTgSS8UyDfD5Ag9sOJU:1wJpoy:upFM-sZK6RCWnPmcAs9okhm74BG9RGzLnk9VwcZP81A', '2026-05-18 16:42:36.359872+07');


--
-- Data for Name: food_store_cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_cart (id, created_at, updated_at, customer_id) VALUES (1, '2026-05-04 16:43:50.739428+07', '2026-05-04 16:43:50.739442+07', 4);


--
-- Data for Name: food_store_cartitem; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: food_store_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_category (id, name, description, image) VALUES (1, 'Rau củ quả', 'Rau củ quả tươi sạch', '');
INSERT INTO public.food_store_category (id, name, description, image) VALUES (2, 'Trái cây', 'Trái cây tươi ngon', '');
INSERT INTO public.food_store_category (id, name, description, image) VALUES (3, 'Thịt cá', 'Thịt cá tươi sống', '');
INSERT INTO public.food_store_category (id, name, description, image) VALUES (4, 'Gạo - Ngũ cốc', 'Gạo và ngũ cốc dinh dưỡng', '');
INSERT INTO public.food_store_category (id, name, description, image) VALUES (5, 'Đồ uống', 'Nước ép, sữa tươi', '');


--
-- Data for Name: food_store_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_customer (id, phone, address, latitude, longitude, created_at, user_id) VALUES (4, '', '', NULL, NULL, '2026-05-04 16:43:50.735598+07', 1);
INSERT INTO public.food_store_customer (id, phone, address, latitude, longitude, created_at, user_id) VALUES (1, '0912345678', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, '2026-02-18 11:45:40+07', 2);
INSERT INTO public.food_store_customer (id, phone, address, latitude, longitude, created_at, user_id) VALUES (2, '0912345679', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, '2026-03-02 16:06:44+07', 3);
INSERT INTO public.food_store_customer (id, phone, address, latitude, longitude, created_at, user_id) VALUES (3, '0912345680', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, '2026-03-11 11:10:38+07', 4);


--
-- Data for Name: food_store_deliveryzone; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_deliveryzone (id, name, area_description, delivery_fee, delivery_time, is_active) VALUES (1, 'Quận 1', '', 15000.00, '', true);
INSERT INTO public.food_store_deliveryzone (id, name, area_description, delivery_fee, delivery_time, is_active) VALUES (2, 'Quận 3', '', 15000.00, '', true);
INSERT INTO public.food_store_deliveryzone (id, name, area_description, delivery_fee, delivery_time, is_active) VALUES (3, 'Bình Thạnh', '', 20000.00, '', true);
INSERT INTO public.food_store_deliveryzone (id, name, area_description, delivery_fee, delivery_time, is_active) VALUES (4, 'Quận 5', '', 18000.00, '', true);


--
-- Data for Name: food_store_emailverification; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: food_store_farm; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_farm (id, name, address, phone, email, description, latitude, longitude, organic_certified, certification_number, created_at, updated_at) VALUES (1, 'Cửa hàng Quận 1', '123 Nguyễn Huệ, Quận 1, TP.HCM', '0901234567', '', '', 10.7769, 106.7009, false, '', '2026-03-01 09:00:00+07', '2026-05-04 16:53:43.975578+07');
INSERT INTO public.food_store_farm (id, name, address, phone, email, description, latitude, longitude, organic_certified, certification_number, created_at, updated_at) VALUES (2, 'Cửa hàng Quận 3', '456 Võ Văn Tần, Quận 3, TP.HCM', '0901234568', '', '', 10.7823, 106.6917, false, '', '2026-03-05 10:30:00+07', '2026-05-04 16:53:43.985648+07');
INSERT INTO public.food_store_farm (id, name, address, phone, email, description, latitude, longitude, organic_certified, certification_number, created_at, updated_at) VALUES (3, 'Cửa hàng Bình Thạnh', '789 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP.HCM', '0901234569', '', '', 10.8142, 106.7012, false, '', '2026-03-08 14:00:00+07', '2026-05-04 16:53:43.987504+07');


--
-- Data for Name: food_store_inventoryreport; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (1, '2026-03-31', 14, 1055, 35850000.00, 'Kiểm kê cuối tháng 3/2026 - Cửa hàng Quận 1', '2026-04-01 08:00:00+07', 8, 1);
INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (2, '2026-03-31', 14, 380, 12450000.00, 'Kiểm kê cuối tháng 3/2026 - Cửa hàng Quận 3', '2026-04-01 08:30:00+07', 9, 2);
INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (3, '2026-03-31', 14, 360, 11280000.00, 'Kiểm kê cuối tháng 3/2026 - Cửa hàng Bình Thạnh', '2026-04-01 09:00:00+07', 10, 3);
INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (4, '2026-04-30', 14, 1120, 37200000.00, 'Kiểm kê cuối tháng 4/2026 - Cửa hàng Quận 1', '2026-05-01 08:00:00+07', 8, 1);
INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (5, '2026-04-30', 14, 420, 13850000.00, 'Kiểm kê cuối tháng 4/2026 - Cửa hàng Quận 3', '2026-05-01 08:30:00+07', 9, 2);
INSERT INTO public.food_store_inventoryreport (id, report_date, total_products, total_quantity, total_value, notes, created_at, created_by_id, farm_id) VALUES (6, '2026-04-30', 14, 390, 12150000.00, 'Kiểm kê cuối tháng 4/2026 - Cửa hàng Bình Thạnh', '2026-05-01 09:00:00+07', 10, 3);



--
-- Data for Name: food_store_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (353, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 128000.00, '2026-02-16 09:59:25+07', '2026-05-04 17:02:42.604169+07', '2026-02-18 15:18:25+07', '', 1, 4, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-16 10:17:25+07', '', '2026-02-16 11:59:25+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (354, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 235000.00, '2026-02-16 16:13:46+07', '2026-05-04 17:02:42.605901+07', '2026-02-19 06:40:46+07', '', 3, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-16 16:21:46+07', '', '2026-02-16 17:13:46+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (355, 'delivered', '', NULL, NULL, 15000.00, 30000.00, '2026-02-17 14:11:27+07', '2026-05-04 17:02:42.607499+07', '2026-02-19 05:42:27+07', '', 4, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-17 14:35:27+07', '', '2026-02-17 15:11:27+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (356, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 263000.00, '2026-02-18 17:11:40+07', '2026-05-04 17:02:42.608903+07', '2026-02-20 11:42:40+07', '', 1, 4, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-18 17:34:40+07', '', '2026-02-18 18:11:40+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (357, 'delivered', '', NULL, NULL, 20000.00, 491000.00, '2026-02-19 08:46:24+07', '2026-05-04 17:02:42.610752+07', '2026-02-21 04:43:24+07', '', 4, 3, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-02-19 09:14:24+07', '', '2026-02-19 09:46:24+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (358, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 216000.00, '2026-02-19 19:10:39+07', '2026-05-04 17:02:42.61236+07', '2026-02-21 02:39:39+07', '', 1, 4, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-19 19:35:39+07', '', '2026-02-19 22:10:39+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (359, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 340000.00, '2026-02-19 20:07:35+07', '2026-05-04 17:02:42.614491+07', '2026-02-21 15:24:35+07', '', 2, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-19 20:12:35+07', '', '2026-02-19 22:07:35+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (360, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 488000.00, '2026-02-20 11:19:33+07', '2026-05-04 17:02:42.616122+07', '2026-02-22 16:17:33+07', '', 1, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-02-20 11:48:33+07', '', '2026-02-20 13:19:33+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (361, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 105000.00, '2026-02-20 11:59:50+07', '2026-05-04 17:02:42.617527+07', '2026-02-21 20:37:50+07', '', 2, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-20 12:25:50+07', '', '2026-02-20 13:59:50+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (362, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 342000.00, '2026-02-20 12:27:48+07', '2026-05-04 17:02:42.618879+07', '2026-02-21 23:50:48+07', '', 3, 2, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-20 12:47:48+07', '', '2026-02-20 14:27:48+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (363, 'delivered', '', NULL, NULL, 15000.00, 240000.00, '2026-02-20 13:18:01+07', '2026-05-04 17:02:42.621828+07', '2026-02-23 00:54:01+07', '', 4, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-20 13:41:01+07', '', '2026-02-20 15:18:01+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (364, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 63000.00, '2026-02-20 13:33:36+07', '2026-05-04 17:02:42.624081+07', '2026-02-23 10:01:36+07', '', 2, 4, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-20 13:41:36+07', '', '2026-02-20 16:33:36+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (365, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 60000.00, '2026-02-20 16:41:58+07', '2026-05-04 17:02:42.625982+07', '2026-02-23 01:08:58+07', '', 2, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-20 16:52:58+07', '', '2026-02-20 19:41:58+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (366, 'delivered', '', NULL, NULL, 18000.00, 78000.00, '2026-02-21 12:23:54+07', '2026-05-04 17:02:42.627748+07', '2026-02-23 22:57:54+07', '', 4, 4, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-21 12:41:54+07', '', '2026-02-21 14:23:54+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (367, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 435000.00, '2026-02-23 18:45:35+07', '2026-05-04 17:02:42.629245+07', '2026-02-25 02:38:35+07', '', 3, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-23 19:11:35+07', '', '2026-02-23 21:45:35+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (368, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 496000.00, '2026-02-23 18:45:40+07', '2026-05-04 17:02:42.631084+07', '2026-02-26 04:22:40+07', '', 3, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-23 19:10:40+07', '', '2026-02-23 21:45:40+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (369, 'delivered', '', NULL, NULL, 15000.00, 275000.00, '2026-02-24 12:10:24+07', '2026-05-04 17:02:42.632573+07', '2026-02-25 20:27:24+07', '', 4, 2, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-02-24 12:22:24+07', '', '2026-02-24 15:10:24+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (370, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 592000.00, '2026-02-24 14:05:06+07', '2026-05-04 17:02:42.634604+07', '2026-02-27 05:33:06+07', '', 3, 2, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-02-24 14:33:06+07', '', '2026-02-24 17:05:06+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (371, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 439000.00, '2026-02-24 18:48:28+07', '2026-05-04 17:02:42.636276+07', '2026-02-25 19:57:28+07', '', 3, 2, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-24 18:54:28+07', '', '2026-02-24 19:48:28+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (372, 'delivered', '', NULL, NULL, 15000.00, 75000.00, '2026-02-25 13:13:55+07', '2026-05-04 17:02:42.637757+07', '2026-02-27 08:26:55+07', '', 4, 2, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-25 13:19:55+07', '', '2026-02-25 16:13:55+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (373, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 723000.00, '2026-02-25 14:51:33+07', '2026-05-04 17:02:42.639077+07', '2026-02-28 03:53:33+07', '', 2, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-25 15:16:33+07', '', '2026-02-25 15:51:33+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (374, 'delivered', '', NULL, NULL, 15000.00, 196000.00, '2026-02-26 10:47:03+07', '2026-05-04 17:02:42.641296+07', '2026-02-27 14:06:03+07', '', 4, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-26 11:00:03+07', '', '2026-02-26 13:47:03+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (375, 'delivered', '', NULL, NULL, 20000.00, 153000.00, '2026-02-27 12:27:49+07', '2026-05-04 17:02:42.643386+07', '2026-03-02 08:03:49+07', '', 4, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-02-27 12:37:49+07', '', '2026-02-27 15:27:49+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (376, 'delivered', '', NULL, NULL, 20000.00, 185000.00, '2026-02-28 15:32:26+07', '2026-05-04 17:02:42.645154+07', '2026-03-02 23:38:26+07', '', 4, 3, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-02-28 15:45:26+07', '', '2026-02-28 16:32:26+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (377, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 55000.00, '2026-03-02 11:34:40+07', '2026-05-04 17:02:42.646688+07', '2026-03-04 16:33:40+07', '', 2, 2, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-02 12:03:40+07', '', '2026-03-02 13:34:40+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (378, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 233000.00, '2026-03-02 20:31:18+07', '2026-05-04 17:02:42.648097+07', '2026-03-04 20:45:18+07', '', 3, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-02 20:47:18+07', '', '2026-03-02 21:31:18+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (379, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 72000.00, '2026-03-03 15:10:07+07', '2026-05-04 17:02:42.650052+07', '2026-03-06 13:03:07+07', '', 2, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-03 15:33:07+07', '', '2026-03-03 17:10:07+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (380, 'delivered', '', NULL, NULL, 18000.00, 357000.00, '2026-03-04 11:55:55+07', '2026-05-04 17:02:42.651573+07', '2026-03-06 07:12:55+07', '', 4, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-04 12:12:55+07', '', '2026-03-04 13:55:55+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (381, 'delivered', '', NULL, NULL, 20000.00, 425000.00, '2026-03-04 20:48:11+07', '2026-05-04 17:02:42.652957+07', '2026-03-07 14:39:11+07', '', 4, 3, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-04 21:13:11+07', '', '2026-03-04 23:48:11+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (382, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 28000.00, '2026-03-05 14:38:30+07', '2026-05-04 17:02:42.654864+07', '2026-03-08 12:17:30+07', '', 1, 3, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-05 15:01:30+07', '', '2026-03-05 16:38:30+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (383, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 733000.00, '2026-03-08 08:17:36+07', '2026-05-04 17:02:42.656465+07', '2026-03-09 17:26:36+07', '', 3, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-08 08:47:36+07', '', '2026-03-08 10:17:36+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (384, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 221000.00, '2026-03-08 09:03:16+07', '2026-05-04 17:02:42.657976+07', '2026-03-10 02:17:16+07', '', 3, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-08 09:33:16+07', '', '2026-03-08 12:03:16+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (385, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 95000.00, '2026-03-08 12:43:01+07', '2026-05-04 17:02:42.65925+07', '2026-03-10 01:52:01+07', '', 3, 2, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-08 12:50:01+07', '', '2026-03-08 13:43:01+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (386, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 283000.00, '2026-03-09 13:28:39+07', '2026-05-04 17:02:42.660297+07', '2026-03-11 15:37:39+07', '', 1, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-09 13:48:39+07', '', '2026-03-09 15:28:39+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (387, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 77000.00, '2026-03-09 13:55:02+07', '2026-05-04 17:02:42.66183+07', '2026-03-11 22:24:02+07', '', 2, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-09 14:24:02+07', '', '2026-03-09 16:55:02+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (388, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 566000.00, '2026-03-09 15:24:11+07', '2026-05-04 17:02:42.663144+07', '2026-03-11 04:08:11+07', '', 3, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-09 15:30:11+07', '', '2026-03-09 18:24:11+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (426, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 223000.00, '2026-04-06 15:51:51+07', '2026-05-04 17:02:42.74092+07', '2026-04-08 07:23:51+07', '', 1, 4, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-06 16:01:51+07', '', '2026-04-06 17:51:51+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (352, 'delivered', '', NULL, NULL, 20000.00, 174000.00, '2026-02-15 16:37:12+07', '2026-05-04 17:02:42.600889+07', '2026-02-18 00:35:12+07', '', 4, 3, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-02-15 16:56:12+07', '', '2026-02-15 19:37:12+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (390, 'delivered', '', NULL, NULL, 20000.00, 245000.00, '2026-03-10 17:19:28+07', '2026-05-04 17:02:42.667226+07', '2026-03-12 00:05:28+07', '', 4, 3, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-10 17:34:28+07', '', '2026-03-10 19:19:28+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (391, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 205000.00, '2026-03-11 09:06:30+07', '2026-05-04 17:02:42.669327+07', '2026-03-14 06:22:30+07', '', 2, 1, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-11 09:25:30+07', '', '2026-03-11 11:06:30+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (392, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 276000.00, '2026-03-12 09:25:15+07', '2026-05-04 17:02:42.671468+07', '2026-03-14 07:52:15+07', '', 2, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-12 09:32:15+07', '', '2026-03-12 11:25:15+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (393, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 196000.00, '2026-03-12 20:49:26+07', '2026-05-04 17:02:42.672984+07', '2026-03-14 13:50:26+07', '', 2, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-12 21:17:26+07', '', '2026-03-12 22:49:26+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (394, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 450000.00, '2026-03-14 12:50:25+07', '2026-05-04 17:02:42.674375+07', '2026-03-16 16:27:25+07', '', 3, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-14 13:08:25+07', '', '2026-03-14 13:50:25+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (395, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 160000.00, '2026-03-14 19:50:47+07', '2026-05-04 17:02:42.676186+07', '2026-03-16 01:46:47+07', '', 3, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-14 20:00:47+07', '', '2026-03-14 21:50:47+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (396, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 663000.00, '2026-03-14 20:43:22+07', '2026-05-04 17:02:42.677619+07', '2026-03-16 17:14:22+07', '', 1, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-14 21:05:22+07', '', '2026-03-14 23:43:22+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (397, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 460000.00, '2026-03-15 09:06:54+07', '2026-05-04 17:02:42.678931+07', '2026-03-18 08:03:54+07', '', 3, 1, 1, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-15 09:21:54+07', '', '2026-03-15 10:06:54+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (398, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 290000.00, '2026-03-15 12:06:29+07', '2026-05-04 17:02:42.68033+07', '2026-03-18 01:28:29+07', '', 3, 3, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-15 12:27:29+07', '', '2026-03-15 13:06:29+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (399, 'delivered', '', NULL, NULL, 18000.00, 668000.00, '2026-03-16 12:34:19+07', '2026-05-04 17:02:42.681697+07', '2026-03-18 03:50:19+07', '', 4, 4, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-16 12:52:19+07', '', '2026-03-16 14:34:19+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (400, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 78000.00, '2026-03-16 15:08:10+07', '2026-05-04 17:02:42.683788+07', '2026-03-18 02:03:10+07', '', 1, 1, 1, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-16 15:14:10+07', '', '2026-03-16 17:08:10+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (401, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 313000.00, '2026-03-17 19:29:23+07', '2026-05-04 17:02:42.685371+07', '2026-03-19 11:53:23+07', '', 1, 3, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-17 19:46:23+07', '', '2026-03-17 21:29:23+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (402, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 93000.00, '2026-03-17 20:32:35+07', '2026-05-04 17:02:42.686998+07', '2026-03-20 11:55:35+07', '', 2, 4, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-17 20:41:35+07', '', '2026-03-17 23:32:35+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (403, 'delivered', '', NULL, NULL, 15000.00, 286000.00, '2026-03-18 19:08:05+07', '2026-05-04 17:02:42.688847+07', '2026-03-20 13:42:05+07', '', 4, 2, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-18 19:27:05+07', '', '2026-03-18 21:08:05+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (404, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 216000.00, '2026-03-19 15:15:05+07', '2026-05-04 17:02:42.690974+07', '2026-03-21 11:09:05+07', '', 2, 3, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-19 15:22:05+07', '', '2026-03-19 17:15:05+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (405, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 225000.00, '2026-03-19 16:10:19+07', '2026-05-04 17:02:42.692987+07', '2026-03-22 03:51:19+07', '', 1, 3, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-19 16:34:19+07', '', '2026-03-19 17:10:19+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (406, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 655000.00, '2026-03-19 16:40:43+07', '2026-05-04 17:02:42.694821+07', '2026-03-21 16:43:43+07', '', 3, 1, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-19 17:10:43+07', '', '2026-03-19 17:40:43+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (407, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 135000.00, '2026-03-20 15:33:32+07', '2026-05-04 17:02:42.697204+07', '2026-03-22 15:44:32+07', '', 3, 3, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-20 15:40:32+07', '', '2026-03-20 18:33:32+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (408, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 298000.00, '2026-03-21 08:18:00+07', '2026-05-04 17:02:42.699128+07', '2026-03-23 02:56:00+07', '', 2, 1, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-21 08:41:00+07', '', '2026-03-21 11:18:00+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (409, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 157000.00, '2026-03-21 11:56:17+07', '2026-05-04 17:02:42.70111+07', '2026-03-24 03:09:17+07', '', 2, 4, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-21 12:07:17+07', '', '2026-03-21 13:56:17+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (410, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 288000.00, '2026-03-23 14:54:04+07', '2026-05-04 17:02:42.703+07', '2026-03-25 22:51:04+07', '', 1, 3, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-23 15:24:04+07', '', '2026-03-23 17:54:04+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (411, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 455000.00, '2026-03-23 20:36:21+07', '2026-05-04 17:02:42.705569+07', '2026-03-24 20:56:21+07', '', 2, 3, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-23 20:41:21+07', '', '2026-03-23 21:36:21+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (412, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 151000.00, '2026-03-24 15:05:06+07', '2026-05-04 17:02:42.707948+07', '2026-03-25 21:43:06+07', '', 3, 3, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-24 15:31:06+07', '', '2026-03-24 17:05:06+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (413, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 195000.00, '2026-03-26 19:50:43+07', '2026-05-04 17:02:42.709997+07', '2026-03-28 20:57:43+07', '', 3, 2, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-26 20:20:43+07', '', '2026-03-26 22:50:43+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (414, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 241000.00, '2026-03-27 08:06:53+07', '2026-05-04 17:02:42.712478+07', '2026-03-30 02:52:53+07', '', 3, 1, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-03-27 08:34:53+07', '', '2026-03-27 09:06:53+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (415, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 226000.00, '2026-03-30 19:32:36+07', '2026-05-04 17:02:42.714527+07', '2026-04-01 17:34:36+07', '', 2, 3, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-30 19:58:36+07', '', '2026-03-30 20:32:36+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (416, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 345000.00, '2026-03-31 08:27:39+07', '2026-05-04 17:02:42.716416+07', '2026-04-01 18:20:39+07', '', 3, 1, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-31 08:35:39+07', '', '2026-03-31 10:27:39+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (417, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 904000.00, '2026-03-31 09:55:53+07', '2026-05-04 17:02:42.718922+07', '2026-04-01 17:30:53+07', '', 1, 2, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-31 10:17:53+07', '', '2026-03-31 12:55:53+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (418, 'delivered', '', NULL, NULL, 20000.00, 50000.00, '2026-03-31 10:51:56+07', '2026-05-04 17:02:42.721312+07', '2026-04-03 01:42:56+07', '', 4, 3, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-31 11:19:56+07', '', '2026-03-31 13:51:56+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (419, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 105000.00, '2026-03-31 16:50:08+07', '2026-05-04 17:02:42.723233+07', '2026-04-02 08:05:08+07', '', 2, 3, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-03-31 17:04:08+07', '', '2026-03-31 18:50:08+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (420, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 530000.00, '2026-04-01 20:42:56+07', '2026-05-04 17:02:42.726095+07', '2026-04-03 05:58:56+07', '', 3, 3, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-01 20:56:56+07', '', '2026-04-01 21:42:56+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (421, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 195000.00, '2026-04-02 17:05:37+07', '2026-05-04 17:02:42.72873+07', '2026-04-04 20:26:37+07', '', 3, 3, 2, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-02 17:34:37+07', '', '2026-04-02 20:05:37+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (422, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 220000.00, '2026-04-03 11:06:55+07', '2026-05-04 17:02:42.731419+07', '2026-04-04 23:30:55+07', '', 1, 2, 2, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-03 11:32:55+07', '', '2026-04-03 12:06:55+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (423, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 110000.00, '2026-04-04 13:41:09+07', '2026-05-04 17:02:42.734129+07', '2026-04-06 23:27:09+07', '', 3, 3, 2, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-04 13:53:09+07', '', '2026-04-04 14:41:09+07', 2);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (424, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 240000.00, '2026-04-04 16:26:51+07', '2026-05-04 17:02:42.736165+07', '2026-04-06 15:24:51+07', '', 1, 2, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-04 16:32:51+07', '', '2026-04-04 17:26:51+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (389, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 188000.00, '2026-03-09 19:04:36+07', '2026-05-04 17:02:42.665318+07', '2026-03-11 02:50:36+07', '', 2, 4, 1, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-03-09 19:23:36+07', '', '2026-03-09 21:04:36+07', 1);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (427, 'delivered', '', NULL, NULL, 18000.00, 203000.00, '2026-04-07 08:38:19+07', '2026-05-04 17:02:42.742842+07', '2026-04-10 08:05:19+07', '', 4, 4, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-07 08:55:19+07', '', '2026-04-07 09:38:19+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (428, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 63000.00, '2026-04-07 09:06:37+07', '2026-05-04 17:02:42.745388+07', '2026-04-09 20:08:37+07', '', 3, 4, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-07 09:18:37+07', '', '2026-04-07 11:06:37+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (445, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 35000.00, '2026-04-21 10:20:30+07', '2026-05-04 17:02:42.789983+07', '2026-04-22 11:25:30+07', '', 1, 3, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-21 10:43:30+07', '', '2026-04-21 11:20:30+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (429, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 440000.00, '2026-04-07 12:15:18+07', '2026-05-04 17:02:42.74861+07', '2026-04-08 14:37:18+07', '', 1, 2, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-07 12:29:18+07', '', '2026-04-07 13:15:18+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (430, 'delivered', '', NULL, NULL, 15000.00, 33000.00, '2026-04-07 14:25:31+07', '2026-05-04 17:02:42.751813+07', '2026-04-10 08:24:31+07', '', 4, 2, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-07 14:39:31+07', '', '2026-04-07 15:25:31+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (431, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 71000.00, '2026-04-09 19:25:26+07', '2026-05-04 17:02:42.754528+07', '2026-04-12 12:57:26+07', '', 2, 1, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-09 19:52:26+07', '', '2026-04-09 22:25:26+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (432, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 255000.00, '2026-04-12 13:46:09+07', '2026-05-04 17:02:42.757145+07', '2026-04-13 18:00:09+07', '', 3, 3, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-12 14:07:09+07', '', '2026-04-12 14:46:09+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (433, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 253000.00, '2026-04-13 12:54:56+07', '2026-05-04 17:02:42.75995+07', '2026-04-16 01:37:56+07', '', 3, 3, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-13 13:16:56+07', '', '2026-04-13 15:54:56+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (434, 'delivered', '', NULL, NULL, 15000.00, 45000.00, '2026-04-13 13:07:58+07', '2026-05-04 17:02:42.762765+07', '2026-04-15 08:13:58+07', '', 4, 1, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-13 13:17:58+07', '', '2026-04-13 16:07:58+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (435, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 584000.00, '2026-04-14 19:08:55+07', '2026-05-04 17:02:42.765057+07', '2026-04-16 13:06:55+07', '', 2, 3, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-14 19:23:55+07', '', '2026-04-14 22:08:55+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (436, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 85000.00, '2026-04-16 10:09:51+07', '2026-05-04 17:02:42.767877+07', '2026-04-18 13:24:51+07', '', 1, 2, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-16 10:20:51+07', '', '2026-04-16 11:09:51+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (437, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 18000.00, 178000.00, '2026-04-17 18:14:25+07', '2026-05-04 17:02:42.770649+07', '2026-04-18 18:16:25+07', '', 3, 4, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-17 18:22:25+07', '', '2026-04-17 21:14:25+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (438, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 148000.00, '2026-04-18 09:34:02+07', '2026-05-04 17:02:42.773249+07', '2026-04-21 07:55:02+07', '', 1, 2, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-18 09:43:02+07', '', '2026-04-18 12:34:02+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (439, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 405000.00, '2026-04-18 12:43:11+07', '2026-05-04 17:02:42.775708+07', '2026-04-20 16:48:11+07', '', 3, 3, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-18 13:06:11+07', '', '2026-04-18 15:43:11+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (440, 'delivered', '', NULL, NULL, 15000.00, 135000.00, '2026-04-19 09:28:49+07', '2026-05-04 17:02:42.778187+07', '2026-04-21 07:26:49+07', '', 4, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-19 09:44:49+07', '', '2026-04-19 12:28:49+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (441, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 245000.00, '2026-04-19 12:07:17+07', '2026-05-04 17:02:42.780859+07', '2026-04-20 17:43:17+07', '', 3, 2, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-19 12:27:17+07', '', '2026-04-19 14:07:17+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (442, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 253000.00, '2026-04-19 15:29:00+07', '2026-05-04 17:02:42.782916+07', '2026-04-21 16:36:00+07', '', 2, 4, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-19 15:49:00+07', '', '2026-04-19 16:29:00+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (443, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 550000.00, '2026-04-20 10:42:16+07', '2026-05-04 17:02:42.785113+07', '2026-04-22 11:42:16+07', '', 3, 3, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-20 10:52:16+07', '', '2026-04-20 11:42:16+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (444, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 31000.00, '2026-04-21 08:19:52+07', '2026-05-04 17:02:42.787808+07', '2026-04-22 19:58:52+07', '', 1, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-21 08:44:52+07', '', '2026-04-21 09:19:52+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (446, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 539000.00, '2026-04-21 15:40:21+07', '2026-05-04 17:02:42.791947+07', '2026-04-23 19:58:21+07', '', 2, 4, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-21 15:56:21+07', '', '2026-04-21 16:40:21+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (447, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 480000.00, '2026-04-23 14:40:43+07', '2026-05-04 17:02:42.794075+07', '2026-04-26 13:18:43+07', '', 1, 3, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-23 14:50:43+07', '', '2026-04-23 15:40:43+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (448, 'delivered', '', NULL, NULL, 18000.00, 528000.00, '2026-04-24 16:44:17+07', '2026-05-04 17:02:42.796552+07', '2026-04-27 02:41:17+07', '', 4, 4, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-24 17:10:17+07', '', '2026-04-24 19:44:17+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (449, 'delivered', '', NULL, NULL, 15000.00, 296000.00, '2026-04-24 18:36:10+07', '2026-05-04 17:02:42.799562+07', '2026-04-27 13:01:10+07', '', 4, 2, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-24 19:05:10+07', '', '2026-04-24 21:36:10+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (450, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 327000.00, '2026-04-25 09:13:53+07', '2026-05-04 17:02:42.802273+07', '2026-04-27 03:17:53+07', '', 1, 3, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-25 09:30:53+07', '', '2026-04-25 12:13:53+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (451, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 275000.00, '2026-04-25 19:32:01+07', '2026-05-04 17:02:42.804758+07', '2026-04-28 08:29:01+07', '', 3, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-25 19:49:01+07', '', '2026-04-25 20:32:01+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (452, 'delivered', '', NULL, NULL, 15000.00, 228000.00, '2026-04-26 12:11:57+07', '2026-05-04 17:02:42.807111+07', '2026-04-28 01:04:57+07', '', 4, 2, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-26 12:34:57+07', '', '2026-04-26 13:11:57+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (453, 'delivered', '', NULL, NULL, 15000.00, 105000.00, '2026-04-26 13:38:39+07', '2026-05-04 17:02:42.809234+07', '2026-04-28 07:30:39+07', '', 4, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-26 13:56:39+07', '', '2026-04-26 16:38:39+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (454, 'delivered', '', NULL, NULL, 18000.00, 383000.00, '2026-04-27 11:46:33+07', '2026-05-04 17:02:42.810973+07', '2026-04-30 08:22:33+07', '', 4, 4, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-27 12:15:33+07', '', '2026-04-27 14:46:33+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (455, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 20000.00, 660000.00, '2026-04-27 13:51:39+07', '2026-05-04 17:02:42.812763+07', '2026-04-29 15:00:39+07', '', 3, 3, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-27 14:05:39+07', '', '2026-04-27 15:51:39+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (456, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 15000.00, 210000.00, '2026-04-27 17:26:17+07', '2026-05-04 17:02:42.81574+07', '2026-04-29 07:22:17+07', '', 1, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'paid', '', '2026-04-27 17:39:17+07', '', '2026-04-27 19:26:17+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (457, 'delivered', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 155000.00, '2026-04-27 20:13:12+07', '2026-05-04 17:02:42.818193+07', '2026-04-29 12:16:12+07', '', 3, 1, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-27 20:40:12+07', '', '2026-04-27 21:13:12+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (458, 'delivered', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 38000.00, '2026-04-27 20:19:50+07', '2026-05-04 17:02:42.82083+07', '2026-04-30 04:16:50+07', '', 1, 3, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-27 20:40:50+07', '', '2026-04-27 22:19:50+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (459, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 233000.00, '2026-04-28 11:19:02+07', '2026-05-04 17:02:42.823376+07', '2026-04-30 02:16:02+07', '', 2, 4, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-04-28 11:40:02+07', '', '2026-04-28 13:19:02+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (460, 'delivered', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 20000.00, 145000.00, '2026-04-29 12:15:55+07', '2026-05-04 17:02:42.825636+07', '2026-05-01 14:40:55+07', '', 2, 3, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-29 12:23:55+07', '', '2026-04-29 14:15:55+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (461, 'shipping', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 18000.00, 175000.00, '2026-05-01 09:23:55+07', '2026-05-04 17:02:42.827449+07', '2026-05-02 21:25:05+07', '', 2, 4, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-05-01 09:30:55+07', '', '2026-05-01 11:23:55+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (462, 'shipping', '', NULL, NULL, 15000.00, 60000.00, '2026-05-01 13:43:22+07', '2026-05-04 17:02:42.830055+07', NULL, '', 4, 2, 3, NULL, NULL, 'cod', '', NULL, NULL, 'pending', '', '2026-05-01 14:04:22+07', '', '2026-05-01 14:43:22+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (425, 'delivered', '', NULL, NULL, 15000.00, 566000.00, '2026-04-04 17:23:00+07', '2026-05-04 17:02:42.738781+07', '2026-04-06 05:00:00+07', '', 4, 2, 3, NULL, NULL, 'momo', '', NULL, NULL, 'paid', '', '2026-04-04 17:46:00+07', '', '2026-04-04 19:23:00+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (463, 'shipping', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 18000.00, 218000.00, '2026-05-01 20:08:27+07', '2026-05-04 17:02:42.831753+07', NULL, '', 1, 4, 3, NULL, NULL, 'cod', '', NULL, NULL, 'paid', '', '2026-05-01 20:35:27+07', '', '2026-05-01 22:08:27+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (464, 'shipping', '100 Lê Lợi, Quận 1, TP.HCM', NULL, NULL, 20000.00, 245000.00, '2026-05-02 09:26:51+07', '2026-05-04 17:02:42.833148+07', NULL, '', 1, 3, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'pending', '', '2026-05-02 09:40:51+07', '', '2026-05-02 10:26:51+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (465, 'shipping', '200 Hai Bà Trưng, Quận 3, TP.HCM', NULL, NULL, 15000.00, 698000.00, '2026-05-02 12:11:05+07', '2026-05-04 17:02:42.834932+07', NULL, '', 2, 2, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'pending', '', '2026-05-02 12:20:05+07', '', '2026-05-02 15:11:05+07', 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (466, 'pending', '', NULL, NULL, 15000.00, 220000.00, '2026-05-03 10:02:51+07', '2026-05-04 17:02:42.836814+07', NULL, '', 4, 2, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'pending', '', NULL, '', NULL, 3);
INSERT INTO public.food_store_order (id, status, delivery_address, delivery_latitude, delivery_longitude, delivery_fee, total_amount, created_at, updated_at, delivered_at, notes, customer_id, delivery_zone_id, assigned_farm_id, delivery_distance_km, delivery_duration_min, payment_method, payment_reference, payment_amount, payment_date, payment_status, proof_image, shipper_accepted_at, shipper_notes, shipper_picked_at, assigned_shipper_id) VALUES (467, 'pending', '300 Điện Biên Phủ, Bình Thạnh, TP.HCM', NULL, NULL, 15000.00, 475000.00, '2026-05-03 19:35:36+07', '2026-05-04 17:02:42.838322+07', NULL, '', 3, 1, 3, NULL, NULL, 'bank_transfer', '', NULL, NULL, 'pending', '', '2026-05-03 19:23:36+07', '', '2026-05-03 22:05:36+07', 3);


--
-- Data for Name: food_store_orderitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (887, 3, 18000.00, 352, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (888, 3, 20000.00, 352, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (889, 5, 8000.00, 352, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (890, 5, 22000.00, 353, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (891, 5, 22000.00, 354, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (892, 3, 35000.00, 354, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (893, 1, 15000.00, 355, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (894, 5, 28000.00, 356, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (895, 3, 35000.00, 356, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (896, 2, 28000.00, 357, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (897, 5, 35000.00, 357, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (898, 2, 120000.00, 357, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (899, 2, 8000.00, 358, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (900, 3, 22000.00, 358, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (901, 2, 28000.00, 358, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (902, 4, 15000.00, 358, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (903, 5, 25000.00, 359, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (904, 5, 18000.00, 359, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (905, 5, 22000.00, 359, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (906, 3, 15000.00, 360, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (907, 5, 85000.00, 360, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (908, 2, 45000.00, 361, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (909, 4, 18000.00, 362, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (910, 3, 85000.00, 362, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (911, 5, 45000.00, 363, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (912, 3, 15000.00, 364, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (913, 3, 15000.00, 365, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (914, 4, 15000.00, 366, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (915, 3, 45000.00, 367, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (916, 2, 85000.00, 367, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (917, 2, 15000.00, 367, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (918, 4, 20000.00, 367, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (919, 3, 85000.00, 368, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (920, 4, 28000.00, 368, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (921, 5, 18000.00, 368, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (922, 3, 8000.00, 368, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (923, 2, 15000.00, 369, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (924, 4, 35000.00, 369, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (925, 2, 45000.00, 369, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (926, 5, 28000.00, 370, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (927, 4, 45000.00, 370, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (928, 4, 8000.00, 370, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (929, 5, 45000.00, 370, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (930, 4, 15000.00, 371, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (931, 4, 85000.00, 371, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (932, 3, 8000.00, 371, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (933, 4, 15000.00, 372, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (934, 5, 120000.00, 373, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (935, 1, 28000.00, 373, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (936, 5, 15000.00, 373, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (937, 1, 15000.00, 374, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (938, 3, 18000.00, 374, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (939, 4, 28000.00, 374, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (940, 5, 18000.00, 375, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (941, 1, 35000.00, 375, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (942, 1, 8000.00, 375, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (943, 5, 15000.00, 376, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (944, 2, 45000.00, 376, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (945, 2, 20000.00, 377, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (946, 4, 20000.00, 378, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (947, 3, 45000.00, 378, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (948, 3, 18000.00, 379, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (949, 3, 45000.00, 380, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (950, 3, 35000.00, 380, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (951, 1, 15000.00, 380, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (952, 3, 28000.00, 380, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (953, 2, 15000.00, 381, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (954, 1, 35000.00, 381, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (955, 4, 85000.00, 381, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (956, 1, 8000.00, 382, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (957, 5, 120000.00, 383, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (958, 2, 15000.00, 383, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (959, 1, 85000.00, 383, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (960, 5, 35000.00, 384, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (961, 1, 28000.00, 384, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (962, 4, 20000.00, 385, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (963, 5, 15000.00, 386, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (964, 4, 35000.00, 386, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (965, 2, 25000.00, 386, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (966, 1, 35000.00, 387, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (967, 1, 22000.00, 387, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (968, 3, 25000.00, 388, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (969, 3, 120000.00, 388, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (970, 4, 22000.00, 388, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (971, 1, 28000.00, 388, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (972, 2, 85000.00, 389, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (973, 4, 45000.00, 390, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (974, 3, 15000.00, 390, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (975, 2, 35000.00, 391, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (976, 1, 120000.00, 391, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (977, 4, 45000.00, 392, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (978, 2, 35000.00, 392, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (979, 1, 8000.00, 392, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (980, 1, 85000.00, 393, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (981, 3, 8000.00, 393, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (982, 4, 18000.00, 393, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (983, 5, 28000.00, 394, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (984, 3, 45000.00, 394, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (985, 5, 25000.00, 394, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (986, 1, 35000.00, 394, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (987, 2, 35000.00, 395, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (988, 4, 18000.00, 395, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (989, 5, 120000.00, 396, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (990, 3, 15000.00, 396, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (991, 4, 25000.00, 397, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (992, 2, 45000.00, 397, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (993, 3, 85000.00, 397, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (994, 5, 45000.00, 398, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (995, 3, 15000.00, 398, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (996, 2, 45000.00, 399, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (997, 5, 45000.00, 399, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (998, 3, 85000.00, 399, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (999, 4, 20000.00, 399, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1000, 1, 45000.00, 400, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1001, 1, 18000.00, 400, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1002, 3, 45000.00, 401, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1003, 2, 8000.00, 401, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1004, 2, 15000.00, 401, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1005, 4, 28000.00, 401, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1006, 3, 25000.00, 402, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1007, 1, 25000.00, 403, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1008, 2, 45000.00, 403, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1009, 3, 22000.00, 403, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1010, 5, 18000.00, 403, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1011, 2, 15000.00, 404, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1012, 2, 28000.00, 404, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1013, 2, 25000.00, 404, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1014, 3, 20000.00, 404, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1015, 1, 35000.00, 405, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1016, 2, 85000.00, 405, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1017, 2, 35000.00, 406, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1018, 3, 120000.00, 406, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1019, 5, 15000.00, 406, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1020, 3, 45000.00, 406, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1021, 5, 8000.00, 407, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1022, 5, 15000.00, 407, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1023, 1, 8000.00, 408, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1024, 3, 45000.00, 408, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1025, 2, 25000.00, 408, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1026, 2, 45000.00, 408, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1027, 3, 18000.00, 409, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1028, 1, 85000.00, 409, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1029, 2, 18000.00, 410, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1030, 1, 35000.00, 410, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1031, 1, 85000.00, 410, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1032, 4, 28000.00, 410, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1033, 3, 120000.00, 411, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1034, 5, 15000.00, 411, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1035, 2, 8000.00, 412, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1036, 1, 45000.00, 412, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1037, 2, 35000.00, 412, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1038, 4, 45000.00, 413, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1039, 3, 22000.00, 414, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1040, 4, 25000.00, 414, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1041, 4, 15000.00, 414, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1042, 1, 120000.00, 415, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1043, 2, 8000.00, 415, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1044, 2, 35000.00, 415, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1045, 5, 45000.00, 416, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1046, 2, 35000.00, 416, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1047, 1, 35000.00, 416, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1048, 4, 120000.00, 417, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1049, 2, 22000.00, 417, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1050, 5, 45000.00, 417, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1051, 4, 35000.00, 417, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1052, 2, 15000.00, 418, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1053, 2, 25000.00, 419, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1054, 1, 35000.00, 419, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1055, 1, 25000.00, 420, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1056, 5, 35000.00, 420, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1057, 1, 85000.00, 420, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1058, 5, 45000.00, 420, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1059, 5, 35000.00, 421, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1060, 5, 35000.00, 422, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1061, 2, 15000.00, 422, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1062, 2, 45000.00, 423, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1063, 5, 45000.00, 424, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1064, 3, 35000.00, 425, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1065, 2, 18000.00, 425, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1066, 2, 85000.00, 425, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1067, 2, 120000.00, 425, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1068, 1, 20000.00, 426, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1069, 5, 15000.00, 426, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1070, 5, 22000.00, 426, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1071, 1, 45000.00, 427, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1072, 4, 35000.00, 427, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1073, 3, 15000.00, 428, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1074, 5, 85000.00, 429, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1075, 1, 18000.00, 430, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1076, 2, 28000.00, 431, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1077, 1, 20000.00, 432, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1078, 5, 15000.00, 432, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1079, 4, 35000.00, 432, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1080, 1, 8000.00, 433, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1081, 5, 45000.00, 433, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1082, 2, 15000.00, 434, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1083, 3, 28000.00, 435, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1084, 4, 120000.00, 435, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1085, 2, 35000.00, 436, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1086, 4, 25000.00, 437, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1087, 4, 15000.00, 437, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1088, 1, 8000.00, 438, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1089, 5, 25000.00, 438, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1090, 1, 25000.00, 439, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1091, 1, 45000.00, 439, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1092, 5, 35000.00, 439, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1093, 4, 35000.00, 439, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1094, 1, 45000.00, 440, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1095, 5, 15000.00, 440, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1096, 1, 15000.00, 441, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1097, 5, 35000.00, 441, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1098, 2, 20000.00, 441, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1099, 1, 18000.00, 442, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1100, 4, 8000.00, 442, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1101, 3, 15000.00, 442, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1102, 5, 28000.00, 442, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1103, 2, 85000.00, 443, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1104, 3, 120000.00, 443, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1105, 2, 8000.00, 444, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1106, 1, 15000.00, 445, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1107, 3, 120000.00, 446, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1108, 3, 15000.00, 446, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1109, 2, 28000.00, 446, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1110, 3, 20000.00, 446, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1111, 2, 45000.00, 447, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1112, 4, 85000.00, 447, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1113, 2, 15000.00, 447, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1114, 3, 120000.00, 448, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1115, 3, 35000.00, 448, 12);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1116, 3, 15000.00, 448, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1117, 5, 45000.00, 449, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1118, 2, 28000.00, 449, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1119, 3, 18000.00, 450, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1120, 1, 28000.00, 450, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1121, 3, 45000.00, 450, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1122, 2, 45000.00, 450, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1123, 5, 15000.00, 451, 1);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1124, 5, 25000.00, 451, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1125, 1, 15000.00, 451, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1126, 1, 45000.00, 451, 13);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1127, 1, 35000.00, 452, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1128, 4, 22000.00, 452, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1129, 2, 45000.00, 452, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1130, 2, 45000.00, 453, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1131, 5, 28000.00, 454, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1132, 5, 18000.00, 454, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1133, 1, 85000.00, 454, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1134, 2, 25000.00, 454, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1135, 4, 85000.00, 455, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1136, 3, 25000.00, 455, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1137, 5, 45000.00, 455, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1138, 5, 8000.00, 456, 14);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1139, 1, 15000.00, 456, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1140, 5, 28000.00, 456, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1141, 5, 28000.00, 457, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1142, 1, 18000.00, 458, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1143, 3, 35000.00, 459, 5);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1144, 5, 22000.00, 459, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1145, 5, 25000.00, 460, 2);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1146, 3, 45000.00, 461, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1147, 1, 22000.00, 461, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1148, 3, 15000.00, 462, 8);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1149, 4, 22000.00, 463, 7);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1150, 4, 28000.00, 463, 9);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1151, 5, 45000.00, 464, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1152, 3, 20000.00, 465, 3);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1153, 4, 45000.00, 465, 6);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1154, 5, 85000.00, 465, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1155, 1, 18000.00, 465, 4);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1156, 1, 120000.00, 466, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1157, 1, 85000.00, 466, 11);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1158, 1, 120000.00, 467, 10);
INSERT INTO public.food_store_orderitem (id, quantity, price, order_id, product_id) VALUES (1159, 4, 85000.00, 467, 11);


--
-- Data for Name: food_store_passwordreset; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: food_store_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (1, 'Rau muống', 'Rau muống tươi ngon, chất lượng cao', 15000.00, 'kg', 'products/rau-muong.jpg', 100, true, '', '2026-05-04 16:38:56.543753+07', '2026-05-04 16:42:58.467815+07', 1, 1);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (2, 'Cà chua', 'Cà chua tươi ngon, chất lượng cao', 25000.00, 'kg', 'products/ca-chua-bi.jpg', 80, true, '', '2026-05-04 16:38:56.547977+07', '2026-05-04 16:42:58.471955+07', 1, 1);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (3, 'Cà rót', 'Cà rót tươi ngon, chất lượng cao', 20000.00, 'kg', 'products/ca-rot.jpg', 60, true, '', '2026-05-04 16:38:56.550316+07', '2026-05-04 16:42:58.473571+07', 1, 2);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (4, 'Khoai tây', 'Khoai tây tươi ngon, chất lượng cao', 18000.00, 'kg', 'products/S34fb1352bd3247ec88e25ad56bbf33a74.jpg', 90, true, '', '2026-05-04 16:38:56.552516+07', '2026-05-04 16:42:58.475496+07', 1, 2);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (5, 'Cam sành', 'Cam sành tươi ngon, chất lượng cao', 35000.00, 'kg', 'products/cam-sanh.jpg', 50, true, '', '2026-05-04 16:38:56.555713+07', '2026-05-04 16:42:58.477627+07', 2, 1);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (6, 'Xoài cát Hòa Lộc', 'Xoài cát Hòa Lộc tươi ngon, chất lượng cao', 45000.00, 'kg', 'products/xoai-cat-hoa-loc.jpg', 40, true, '', '2026-05-04 16:38:56.558707+07', '2026-05-04 16:42:58.479245+07', 2, 2);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (7, 'Chuối tiêu', 'Chuối tiêu tươi ngon, chất lượng cao', 22000.00, 'kg', 'products/chuoi-tieu.jpg', 70, true, '', '2026-05-04 16:38:56.561589+07', '2026-05-04 16:42:58.480679+07', 2, 3);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (8, 'Dưa hấu', 'Dưa hấu tươi ngon, chất lượng cao', 15000.00, 'kg', 'products/dua-hau.jpg', 30, true, '', '2026-05-04 16:38:56.564724+07', '2026-05-04 16:42:58.482894+07', 2, 3);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (9, 'Thanh long ruột đỏ', 'Thanh long ruột đỏ tươi ngon, chất lượng cao', 28000.00, 'kg', 'products/thanh-long-ruot-do.jpg', 45, true, '', '2026-05-04 16:38:56.566554+07', '2026-05-04 16:42:58.485076+07', 2, 1);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (10, 'Thịt heo', 'Thịt heo tươi ngon, chất lượng cao', 120000.00, 'kg', 'products/thitheo.jpg', 50, true, '', '2026-05-04 16:38:56.569473+07', '2026-05-04 16:42:58.487347+07', 3, 1);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (11, 'Cá tra', 'Cá tra tươi ngon, chất lượng cao', 85000.00, 'kg', 'products/ca_tra.jpg', 30, true, '', '2026-05-04 16:38:56.571607+07', '2026-05-04 16:42:58.489163+07', 3, 2);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (12, 'Gạo ST25', 'Gạo ST25 tươi ngon, chất lượng cao', 35000.00, 'kg', 'products/gao-st25.jpg', 200, true, '', '2026-05-04 16:38:56.573487+07', '2026-05-04 16:42:58.491589+07', 4, 3);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (13, 'Yến mạch', 'Yến mạch tươi ngon, chất lượng cao', 45000.00, 'kg', 'products/yen-mach.jpg', 100, true, '', '2026-05-04 16:38:56.57707+07', '2026-05-04 16:42:58.493328+07', 4, 2);
INSERT INTO public.food_store_product (id, name, description, price, unit, image, stock_quantity, is_available, nutritional_info, created_at, updated_at, category_id, farm_id) VALUES (14, 'Ít đường 110ml', 'Ít đường 110ml tươi ngon, chất lượng cao', 8000.00, 'chai', 'products/IT-DUONG-110ml.png', 150, true, '', '2026-05-04 16:38:56.579638+07', '2026-05-04 16:42:58.494682+07', 5, 1);


--
-- Data for Name: food_store_shipper; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_shipper (id, phone, vehicle_number, status, total_deliveries, today_deliveries, cod_holding, today_earnings, created_at, updated_at, user_id, assigned_farm_id) VALUES (1, '0923456789', '59A-12345', 'available', 49, 49, 259568.00, 142931.00, '2026-05-04 16:50:35.782474+07', '2026-05-04 17:00:05.685148+07', 5, 1);
INSERT INTO public.food_store_shipper (id, phone, vehicle_number, status, total_deliveries, today_deliveries, cod_holding, today_earnings, created_at, updated_at, user_id, assigned_farm_id) VALUES (2, '0923456790', '59B-67890', 'busy', 23, 23, 93810.00, 80311.00, '2026-05-04 16:50:36.317638+07', '2026-05-04 17:00:05.687174+07', 6, 2);
INSERT INTO public.food_store_shipper (id, phone, vehicle_number, status, total_deliveries, today_deliveries, cod_holding, today_earnings, created_at, updated_at, user_id, assigned_farm_id) VALUES (3, '0923456791', '59C-11111', 'available', 44, 44, 413253.00, 102809.00, '2026-05-04 16:50:36.856928+07', '2026-05-04 17:00:05.689726+07', 7, 3);


--
-- Data for Name: food_store_stockalert; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_stockalert (id, alert_type, threshold, current_stock, is_resolved, resolved_at, resolved_by_id, notes, created_at, farm_id, product_id) VALUES (1, 'low_stock', 50, 30, false, NULL, NULL, 'Tồn kho dưa hấu sắp hết, cần nhập thêm', '2026-05-03 08:00:00+07', 3, 8);
INSERT INTO public.food_store_stockalert (id, alert_type, threshold, current_stock, is_resolved, resolved_at, resolved_by_id, notes, created_at, farm_id, product_id) VALUES (2, 'low_stock', 50, 40, false, NULL, NULL, 'Tồn kho xoài cát sắp hết', '2026-05-03 09:00:00+07', 2, 6);
INSERT INTO public.food_store_stockalert (id, alert_type, threshold, current_stock, is_resolved, resolved_at, resolved_by_id, notes, created_at, farm_id, product_id) VALUES (3, 'low_stock', 50, 30, true, '2026-05-04 10:00:00+07', 8, 'Đã nhập thêm 50kg cá tra', '2026-05-02 14:00:00+07', 2, 11);
INSERT INTO public.food_store_stockalert (id, alert_type, threshold, current_stock, is_resolved, resolved_at, resolved_by_id, notes, created_at, farm_id, product_id) VALUES (4, 'low_stock', 50, 45, false, NULL, NULL, 'Thanh long ruột đỏ cần bổ sung', '2026-05-04 08:30:00+07', 1, 9);



--
-- Data for Name: food_store_stocktransaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Nhập kho từ nhà cung cấp
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (1, 'import', 100, 12000.00, 1200000.00, 0, 100, 'NK001', 'Nhập kho rau muống đầu tiên', '2026-03-01 09:00:00+07', 8, 1, NULL, 1, 1);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (2, 'import', 80, 20000.00, 1600000.00, 0, 80, 'NK002', 'Nhập kho cà chua', '2026-03-01 09:30:00+07', 8, 1, NULL, 2, 1);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (3, 'import', 60, 15000.00, 900000.00, 0, 60, 'NK003', 'Nhập kho cà rót', '2026-03-05 10:30:00+07', 9, 2, NULL, 3, 1);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (4, 'import', 90, 14000.00, 1260000.00, 0, 90, 'NK004', 'Nhập kho khoai tây', '2026-03-05 11:00:00+07', 9, 2, NULL, 4, 1);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (5, 'import', 50, 30000.00, 1500000.00, 0, 50, 'NK005', 'Nhập kho cam sành', '2026-03-01 10:00:00+07', 8, 1, NULL, 5, 2);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (6, 'import', 40, 40000.00, 1600000.00, 0, 40, 'NK006', 'Nhập kho xoài cát Hòa Lộc', '2026-03-05 11:30:00+07', 9, 2, NULL, 6, 2);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (7, 'import', 70, 18000.00, 1260000.00, 0, 70, 'NK007', 'Nhập kho chuối tiêu', '2026-03-08 14:00:00+07', 10, 3, NULL, 7, 2);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (8, 'import', 30, 12000.00, 360000.00, 0, 30, 'NK008', 'Nhập kho dưa hấu', '2026-03-08 14:30:00+07', 10, 3, NULL, 8, 2);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (9, 'import', 45, 25000.00, 1125000.00, 0, 45, 'NK009', 'Nhập kho thanh long ruột đỏ', '2026-03-01 11:00:00+07', 8, 1, NULL, 9, 2);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (10, 'import', 50, 110000.00, 5500000.00, 0, 50, 'NK010', 'Nhập kho thịt heo', '2026-03-01 11:30:00+07', 8, 1, NULL, 10, 3);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (11, 'import', 30, 80000.00, 2400000.00, 0, 30, 'NK011', 'Nhập kho cá tra', '2026-03-05 12:00:00+07', 9, 2, NULL, 11, 3);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (12, 'import', 200, 32000.00, 6400000.00, 0, 200, 'NK012', 'Nhập kho gạo ST25', '2026-03-08 15:00:00+07', 10, 3, NULL, 12, 4);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (13, 'import', 100, 42000.00, 4200000.00, 0, 100, 'NK013', 'Nhập kho yến mạch', '2026-03-05 12:30:00+07', 9, 2, NULL, 13, 4);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (14, 'import', 150, 6000.00, 900000.00, 0, 150, 'NK014', 'Nhập kho nước ít đường', '2026-03-01 12:00:00+07', 8, 1, NULL, 14, 5);

-- Xuất kho theo đơn hàng (một số giao dịch mẫu)
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (15, 'export', -5, 15000.00, 75000.00, 100, 95, 'XK001', 'Xuất kho cho đơn hàng #353', '2026-02-16 10:00:00+07', 8, 1, 353, 1, NULL);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (16, 'export', -3, 25000.00, 75000.00, 80, 77, 'XK002', 'Xuất kho cho đơn hàng #353', '2026-02-16 10:05:00+07', 8, 1, 353, 2, NULL);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (17, 'export', -2, 35000.00, 70000.00, 50, 48, 'XK003', 'Xuất kho cho đơn hàng #354', '2026-02-16 16:15:00+07', 8, 1, 354, 5, NULL);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (18, 'export', -4, 45000.00, 180000.00, 40, 36, 'XK004', 'Xuất kho cho đơn hàng #354', '2026-02-16 16:20:00+07', 9, 2, 354, 6, NULL);

-- Điều chỉnh tồn kho
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (19, 'adjustment', 100, NULL, NULL, 95, 100, 'DC001', 'Điều chỉnh tồn kho sau kiểm kê', '2026-04-01 09:00:00+07', 8, 1, NULL, 1, NULL);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (20, 'adjustment', 80, NULL, NULL, 77, 80, 'DC002', 'Điều chỉnh tồn kho sau kiểm kê', '2026-04-01 09:15:00+07', 8, 1, NULL, 2, NULL);

-- Hàng hư hỏng
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (21, 'damaged', -2, 35000.00, 70000.00, 48, 46, 'HH001', 'Cam sành bị hư do vận chuyển', '2026-04-15 10:00:00+07', 8, 1, NULL, 5, NULL);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (22, 'damaged', -4, 45000.00, 180000.00, 36, 32, 'HH002', 'Xoài cát bị dập', '2026-04-20 11:00:00+07', 9, 2, NULL, 6, NULL);

-- Trả hàng cho nhà cung cấp
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (23, 'return', 8, 45000.00, 360000.00, 32, 40, 'TH001', 'Trả lại xoài cát không đạt chất lượng', '2026-04-22 14:00:00+07', 9, 2, NULL, 6, 2);

-- Nhập kho bổ sung gần đây
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (24, 'import', 50, 80000.00, 4000000.00, 30, 80, 'NK015', 'Nhập bổ sung cá tra', '2026-05-04 08:00:00+07', 9, 2, NULL, 11, 3);
INSERT INTO public.food_store_stocktransaction (id, transaction_type, quantity, unit_price, total_amount, stock_before, stock_after, reference_number, notes, created_at, created_by_id, farm_id, order_id, product_id, supplier_id) VALUES (25, 'import', 30, 12000.00, 360000.00, 30, 60, 'NK016', 'Nhập bổ sung dưa hấu', '2026-05-04 09:00:00+07', 10, 3, NULL, 8, 2);



--
-- Data for Name: food_store_storeadmin; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_storeadmin (id, phone, can_manage_products, can_manage_orders, can_manage_inventory, can_manage_shippers, can_view_reports, is_active, created_at, updated_at, farm_id, user_id) VALUES (1, '0934567890', true, true, true, true, true, true, '2026-05-04 16:50:37.398601+07', '2026-05-04 16:50:37.398611+07', 1, 8);
INSERT INTO public.food_store_storeadmin (id, phone, can_manage_products, can_manage_orders, can_manage_inventory, can_manage_shippers, can_view_reports, is_active, created_at, updated_at, farm_id, user_id) VALUES (2, '0934567891', true, true, true, true, true, true, '2026-05-04 16:50:37.941322+07', '2026-05-04 16:50:37.941329+07', 2, 9);
INSERT INTO public.food_store_storeadmin (id, phone, can_manage_products, can_manage_orders, can_manage_inventory, can_manage_shippers, can_view_reports, is_active, created_at, updated_at, farm_id, user_id) VALUES (3, '0934567892', true, true, true, true, true, true, '2026-05-04 16:50:38.483769+07', '2026-05-04 16:50:38.483776+07', 3, 10);


--
-- Data for Name: food_store_supplier; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.food_store_supplier (id, name, contact_person, phone, email, address, tax_code, notes, is_active, created_at, updated_at) VALUES (1, 'Công ty TNHH Nông sản Sạch Việt', 'Nguyễn Văn An', '0281234567', 'contact@nongsansach.vn', '123 Đường Lê Văn Việt, Quận 9, TP.HCM', '0123456789', 'Nhà cung cấp rau củ quả chính', true, '2026-01-15 08:00:00+07', '2026-05-04 17:00:00+07');
INSERT INTO public.food_store_supplier (id, name, contact_person, phone, email, address, tax_code, notes, is_active, created_at, updated_at) VALUES (2, 'Trang trại Trái cây Miền Nam', 'Trần Thị Bình', '0287654321', 'info@traicaymiennam.vn', '456 Quốc lộ 1A, Tiền Giang', '0987654321', 'Chuyên cung cấp trái cây tươi', true, '2026-01-20 09:30:00+07', '2026-05-04 17:00:00+07');
INSERT INTO public.food_store_supplier (id, name, contact_person, phone, email, address, tax_code, notes, is_active, created_at, updated_at) VALUES (3, 'Cơ sở Thịt sạch Hòa Bình', 'Lê Văn Cường', '0283456789', 'hoabinh@thitsach.vn', '789 Đường Nguyễn Oanh, Gò Vấp, TP.HCM', '0456789123', 'Cung cấp thịt heo, gà, cá', true, '2026-02-01 10:00:00+07', '2026-05-04 17:00:00+07');
INSERT INTO public.food_store_supplier (id, name, contact_person, phone, email, address, tax_code, notes, is_active, created_at, updated_at) VALUES (4, 'Công ty Gạo Ngũ cốc Phương Nam', 'Phạm Thị Dung', '0289876543', 'sales@gaophuongnam.vn', '321 Đường Võ Văn Kiệt, Quận 5, TP.HCM', '0789456123', 'Gạo và ngũ cốc chất lượng cao', true, '2026-02-10 11:00:00+07', '2026-05-04 17:00:00+07');
INSERT INTO public.food_store_supplier (id, name, contact_person, phone, email, address, tax_code, notes, is_active, created_at, updated_at) VALUES (5, 'Nhà máy Nước giải khát Tân Hiệp', 'Hoàng Văn Em', '0285678901', 'tanhiep@beverage.vn', '654 Xa lộ Hà Nội, Quận 2, TP.HCM', '0321654987', 'Đồ uống đóng chai', true, '2026-02-15 14:00:00+07', '2026-05-04 17:00:00+07');



--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 88, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 10, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 22, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 31, true);


--
-- Name: food_store_cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_cart_id_seq', 1, true);


--
-- Name: food_store_cartitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_cartitem_id_seq', 1, false);


--
-- Name: food_store_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_category_id_seq', 5, true);


--
-- Name: food_store_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_customer_id_seq', 4, true);


--
-- Name: food_store_deliveryzone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_deliveryzone_id_seq', 4, true);


--
-- Name: food_store_emailverification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_emailverification_id_seq', 1, false);


--
-- Name: food_store_farm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_farm_id_seq', 3, true);


--
-- Name: food_store_inventoryreport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_inventoryreport_id_seq', 6, true);


--
-- Name: food_store_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_order_id_seq', 467, true);


--
-- Name: food_store_orderitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_orderitem_id_seq', 1159, true);


--
-- Name: food_store_passwordreset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_passwordreset_id_seq', 1, false);


--
-- Name: food_store_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_product_id_seq', 14, true);


--
-- Name: food_store_shipper_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_shipper_id_seq', 3, true);


--
-- Name: food_store_stockalert_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_stockalert_id_seq', 4, true);


--
-- Name: food_store_stocktransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_stocktransaction_id_seq', 25, true);


--
-- Name: food_store_storeadmin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_storeadmin_id_seq', 3, true);


--
-- Name: food_store_supplier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.food_store_supplier_id_seq', 5, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: food_store_cart food_store_cart_customer_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cart
    ADD CONSTRAINT food_store_cart_customer_id_key UNIQUE (customer_id);


--
-- Name: food_store_cart food_store_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cart
    ADD CONSTRAINT food_store_cart_pkey PRIMARY KEY (id);


--
-- Name: food_store_cartitem food_store_cartitem_cart_id_product_id_dfb8b76d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cartitem
    ADD CONSTRAINT food_store_cartitem_cart_id_product_id_dfb8b76d_uniq UNIQUE (cart_id, product_id);


--
-- Name: food_store_cartitem food_store_cartitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cartitem
    ADD CONSTRAINT food_store_cartitem_pkey PRIMARY KEY (id);


--
-- Name: food_store_category food_store_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_category
    ADD CONSTRAINT food_store_category_pkey PRIMARY KEY (id);


--
-- Name: food_store_customer food_store_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_customer
    ADD CONSTRAINT food_store_customer_pkey PRIMARY KEY (id);


--
-- Name: food_store_customer food_store_customer_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_customer
    ADD CONSTRAINT food_store_customer_user_id_key UNIQUE (user_id);


--
-- Name: food_store_deliveryzone food_store_deliveryzone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_deliveryzone
    ADD CONSTRAINT food_store_deliveryzone_pkey PRIMARY KEY (id);


--
-- Name: food_store_emailverification food_store_emailverification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_emailverification
    ADD CONSTRAINT food_store_emailverification_pkey PRIMARY KEY (id);


--
-- Name: food_store_farm food_store_farm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_farm
    ADD CONSTRAINT food_store_farm_pkey PRIMARY KEY (id);


--
-- Name: food_store_inventoryreport food_store_inventoryreport_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_inventoryreport
    ADD CONSTRAINT food_store_inventoryreport_pkey PRIMARY KEY (id);


--
-- Name: food_store_order food_store_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_order
    ADD CONSTRAINT food_store_order_pkey PRIMARY KEY (id);


--
-- Name: food_store_orderitem food_store_orderitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_orderitem
    ADD CONSTRAINT food_store_orderitem_pkey PRIMARY KEY (id);


--
-- Name: food_store_passwordreset food_store_passwordreset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_passwordreset
    ADD CONSTRAINT food_store_passwordreset_pkey PRIMARY KEY (id);


--
-- Name: food_store_product food_store_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_product
    ADD CONSTRAINT food_store_product_pkey PRIMARY KEY (id);


--
-- Name: food_store_shipper food_store_shipper_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_shipper
    ADD CONSTRAINT food_store_shipper_pkey PRIMARY KEY (id);


--
-- Name: food_store_shipper food_store_shipper_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_shipper
    ADD CONSTRAINT food_store_shipper_user_id_key UNIQUE (user_id);


--
-- Name: food_store_stockalert food_store_stockalert_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stockalert
    ADD CONSTRAINT food_store_stockalert_pkey PRIMARY KEY (id);


--
-- Name: food_store_stocktransaction food_store_stocktransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktransaction_pkey PRIMARY KEY (id);


--
-- Name: food_store_storeadmin food_store_storeadmin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_storeadmin
    ADD CONSTRAINT food_store_storeadmin_pkey PRIMARY KEY (id);


--
-- Name: food_store_storeadmin food_store_storeadmin_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_storeadmin
    ADD CONSTRAINT food_store_storeadmin_user_id_key UNIQUE (user_id);


--
-- Name: food_store_supplier food_store_supplier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_supplier
    ADD CONSTRAINT food_store_supplier_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: food_store__created_318c1b_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store__created_318c1b_idx ON public.food_store_stocktransaction USING btree (created_at DESC);


--
-- Name: food_store__farm_id_057a7e_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store__farm_id_057a7e_idx ON public.food_store_stocktransaction USING btree (farm_id, created_at DESC);


--
-- Name: food_store__product_bee5b6_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store__product_bee5b6_idx ON public.food_store_stocktransaction USING btree (product_id, created_at DESC);


--
-- Name: food_store_cartitem_cart_id_4bc929e4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_cartitem_cart_id_4bc929e4 ON public.food_store_cartitem USING btree (cart_id);


--
-- Name: food_store_cartitem_product_id_8d7bed26; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_cartitem_product_id_8d7bed26 ON public.food_store_cartitem USING btree (product_id);


--
-- Name: food_store_inventoryreport_created_by_id_788205b9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_inventoryreport_created_by_id_788205b9 ON public.food_store_inventoryreport USING btree (created_by_id);


--
-- Name: food_store_inventoryreport_farm_id_aaed62d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_inventoryreport_farm_id_aaed62d8 ON public.food_store_inventoryreport USING btree (farm_id);


--
-- Name: food_store_order_assigned_farm_id_9f7bbc41; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_order_assigned_farm_id_9f7bbc41 ON public.food_store_order USING btree (assigned_farm_id);


--
-- Name: food_store_order_assigned_shipper_id_b7958c26; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_order_assigned_shipper_id_b7958c26 ON public.food_store_order USING btree (assigned_shipper_id);


--
-- Name: food_store_order_customer_id_437a55ee; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_order_customer_id_437a55ee ON public.food_store_order USING btree (customer_id);


--
-- Name: food_store_order_delivery_zone_id_1a3f1f54; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_order_delivery_zone_id_1a3f1f54 ON public.food_store_order USING btree (delivery_zone_id);


--
-- Name: food_store_orderitem_order_id_5be5ed12; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_orderitem_order_id_5be5ed12 ON public.food_store_orderitem USING btree (order_id);


--
-- Name: food_store_orderitem_product_id_43e845e6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_orderitem_product_id_43e845e6 ON public.food_store_orderitem USING btree (product_id);


--
-- Name: food_store_passwordreset_user_id_a7819a53; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_passwordreset_user_id_a7819a53 ON public.food_store_passwordreset USING btree (user_id);


--
-- Name: food_store_product_category_id_163e3ba4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_product_category_id_163e3ba4 ON public.food_store_product USING btree (category_id);


--
-- Name: food_store_product_farm_id_df30caee; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_product_farm_id_df30caee ON public.food_store_product USING btree (farm_id);


--
-- Name: food_store_shipper_assigned_farm_id_b497bb82; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_shipper_assigned_farm_id_b497bb82 ON public.food_store_shipper USING btree (assigned_farm_id);


--
-- Name: food_store_stockalert_farm_id_e6249491; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stockalert_farm_id_e6249491 ON public.food_store_stockalert USING btree (farm_id);


--
-- Name: food_store_stockalert_product_id_b4244a82; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stockalert_product_id_b4244a82 ON public.food_store_stockalert USING btree (product_id);


--
-- Name: food_store_stockalert_resolved_by_id_a9ae68ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stockalert_resolved_by_id_a9ae68ac ON public.food_store_stockalert USING btree (resolved_by_id);


--
-- Name: food_store_stocktransaction_created_by_id_43dbae19; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stocktransaction_created_by_id_43dbae19 ON public.food_store_stocktransaction USING btree (created_by_id);


--
-- Name: food_store_stocktransaction_farm_id_493f6ff1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stocktransaction_farm_id_493f6ff1 ON public.food_store_stocktransaction USING btree (farm_id);


--
-- Name: food_store_stocktransaction_order_id_64bb83c3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stocktransaction_order_id_64bb83c3 ON public.food_store_stocktransaction USING btree (order_id);


--
-- Name: food_store_stocktransaction_product_id_84ea055e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stocktransaction_product_id_84ea055e ON public.food_store_stocktransaction USING btree (product_id);


--
-- Name: food_store_stocktransaction_supplier_id_a133701a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_stocktransaction_supplier_id_a133701a ON public.food_store_stocktransaction USING btree (supplier_id);


--
-- Name: food_store_storeadmin_farm_id_572ebddc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX food_store_storeadmin_farm_id_572ebddc ON public.food_store_storeadmin USING btree (farm_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_cart food_store_cart_customer_id_22389329_fk_food_store_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cart
    ADD CONSTRAINT food_store_cart_customer_id_22389329_fk_food_store_customer_id FOREIGN KEY (customer_id) REFERENCES public.food_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_cartitem food_store_cartitem_cart_id_4bc929e4_fk_food_store_cart_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cartitem
    ADD CONSTRAINT food_store_cartitem_cart_id_4bc929e4_fk_food_store_cart_id FOREIGN KEY (cart_id) REFERENCES public.food_store_cart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_cartitem food_store_cartitem_product_id_8d7bed26_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_cartitem
    ADD CONSTRAINT food_store_cartitem_product_id_8d7bed26_fk_food_stor FOREIGN KEY (product_id) REFERENCES public.food_store_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_customer food_store_customer_user_id_6fe6a5ae_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_customer
    ADD CONSTRAINT food_store_customer_user_id_6fe6a5ae_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_inventoryreport food_store_inventory_created_by_id_788205b9_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_inventoryreport
    ADD CONSTRAINT food_store_inventory_created_by_id_788205b9_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_inventoryreport food_store_inventory_farm_id_aaed62d8_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_inventoryreport
    ADD CONSTRAINT food_store_inventory_farm_id_aaed62d8_fk_food_stor FOREIGN KEY (farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_order food_store_order_assigned_farm_id_9f7bbc41_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_order
    ADD CONSTRAINT food_store_order_assigned_farm_id_9f7bbc41_fk_food_stor FOREIGN KEY (assigned_farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_order food_store_order_assigned_shipper_id_b7958c26_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_order
    ADD CONSTRAINT food_store_order_assigned_shipper_id_b7958c26_fk_food_stor FOREIGN KEY (assigned_shipper_id) REFERENCES public.food_store_shipper(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_order food_store_order_customer_id_437a55ee_fk_food_store_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_order
    ADD CONSTRAINT food_store_order_customer_id_437a55ee_fk_food_store_customer_id FOREIGN KEY (customer_id) REFERENCES public.food_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_order food_store_order_delivery_zone_id_1a3f1f54_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_order
    ADD CONSTRAINT food_store_order_delivery_zone_id_1a3f1f54_fk_food_stor FOREIGN KEY (delivery_zone_id) REFERENCES public.food_store_deliveryzone(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_orderitem food_store_orderitem_order_id_5be5ed12_fk_food_store_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_orderitem
    ADD CONSTRAINT food_store_orderitem_order_id_5be5ed12_fk_food_store_order_id FOREIGN KEY (order_id) REFERENCES public.food_store_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_orderitem food_store_orderitem_product_id_43e845e6_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_orderitem
    ADD CONSTRAINT food_store_orderitem_product_id_43e845e6_fk_food_stor FOREIGN KEY (product_id) REFERENCES public.food_store_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_passwordreset food_store_passwordreset_user_id_a7819a53_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_passwordreset
    ADD CONSTRAINT food_store_passwordreset_user_id_a7819a53_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_product food_store_product_category_id_163e3ba4_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_product
    ADD CONSTRAINT food_store_product_category_id_163e3ba4_fk_food_stor FOREIGN KEY (category_id) REFERENCES public.food_store_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_product food_store_product_farm_id_df30caee_fk_food_store_farm_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_product
    ADD CONSTRAINT food_store_product_farm_id_df30caee_fk_food_store_farm_id FOREIGN KEY (farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_shipper food_store_shipper_assigned_farm_id_b497bb82_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_shipper
    ADD CONSTRAINT food_store_shipper_assigned_farm_id_b497bb82_fk_food_stor FOREIGN KEY (assigned_farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_shipper food_store_shipper_user_id_72a33852_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_shipper
    ADD CONSTRAINT food_store_shipper_user_id_72a33852_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stockalert food_store_stockaler_product_id_b4244a82_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stockalert
    ADD CONSTRAINT food_store_stockaler_product_id_b4244a82_fk_food_stor FOREIGN KEY (product_id) REFERENCES public.food_store_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stockalert food_store_stockalert_farm_id_e6249491_fk_food_store_farm_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stockalert
    ADD CONSTRAINT food_store_stockalert_farm_id_e6249491_fk_food_store_farm_id FOREIGN KEY (farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stockalert food_store_stockalert_resolved_by_id_a9ae68ac_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stockalert
    ADD CONSTRAINT food_store_stockalert_resolved_by_id_a9ae68ac_fk_auth_user_id FOREIGN KEY (resolved_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stocktransaction food_store_stocktran_created_by_id_43dbae19_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktran_created_by_id_43dbae19_fk_auth_user FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stocktransaction food_store_stocktran_farm_id_493f6ff1_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktran_farm_id_493f6ff1_fk_food_stor FOREIGN KEY (farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stocktransaction food_store_stocktran_order_id_64bb83c3_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktran_order_id_64bb83c3_fk_food_stor FOREIGN KEY (order_id) REFERENCES public.food_store_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stocktransaction food_store_stocktran_product_id_84ea055e_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktran_product_id_84ea055e_fk_food_stor FOREIGN KEY (product_id) REFERENCES public.food_store_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_stocktransaction food_store_stocktran_supplier_id_a133701a_fk_food_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_stocktransaction
    ADD CONSTRAINT food_store_stocktran_supplier_id_a133701a_fk_food_stor FOREIGN KEY (supplier_id) REFERENCES public.food_store_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_storeadmin food_store_storeadmin_farm_id_572ebddc_fk_food_store_farm_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_storeadmin
    ADD CONSTRAINT food_store_storeadmin_farm_id_572ebddc_fk_food_store_farm_id FOREIGN KEY (farm_id) REFERENCES public.food_store_farm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: food_store_storeadmin food_store_storeadmin_user_id_b28a5e37_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.food_store_storeadmin
    ADD CONSTRAINT food_store_storeadmin_user_id_b28a5e37_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict TQbfbp5hV7RE6rUAnTn64PflKaMYNVeNcUxYh8ymFne2X2tLoLcQdAlRsVjmJvM

