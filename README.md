# Consumer_producer_Python

# Detalii implementare:

Fiecare producer si cart primeste, la inceput un id unic prin care este identficat.

Pentru produceri am folosit 2 liste:
	-o lista ce tine minte cate produse mai poate adauga fiecare producer
	-o lista ce contine produsele inauntru
	accesul in liste se face prin intermediul id-ului primit de la producer

Pentru carturi am folosit o lista
	-o lista ce contine produsele adaugate in cos

Pentru a evita problemele de race condition, am introdus Lock-uri acolo unde era nevoie:
	-atunci cand trebuie sa returnez un id unui producer/cart
	-cand adaug/scot elemente din una dintre liste
	-cand printez output

# Clasa marketplace
	-Contine un constructor, care initializeaza campurile si porneste threadul
	-Functia register_producer: adauga un producer in lista de produceri si ii returneaza un id
	-Functia publish: adauga produsul primit ca parametru in lista de produse. Returneaza adevarat daca
	producerul mai are loc si fals in cazul in care lista de produse este plina
	-Functia new_cart: adauga un cart in lista de carturi si ii returneaza un id
	-Functia add_to_cart: adauga un produs in cart, daca produsul nu a aparut inca/nu exista, returneaza fals
	-Functia remove_from_cart: scoate un produs din cart si il readauga in lista de produse
	-Functia place_order: returneaza lista de produse aferenta cartului si goleste cartul
	-Functia print_cons: printreaza un produs si de catre cine a fost cumparat

# Clasa consumer: 
	-Contine un constructor, care initializeaza campurile si porneste threadul
	-Functia print_carts: printeaza produsele din cart, folosindu-se de marketplace
	-Functia add_product_to_cart: adauga produsul primit ca parametru in cart folosindu-se de marketplace
	-Functia run: efectueaza operatia (descrisa de "type") de "quantity" dati pentru toate 
	produsele din carturi folosind functiile descrise mai sus. La sfarsit, apeleaza print_carts

# Clasa producer:
	-Contine un constructor, care initializeaza campurile si porneste threadul
	-functia run: efectueaza operatia de adaugare de "quantity" dati pentru toate produsele. 
	Cicleaza pana la terminarea celorlalte threaduri

Tema retine si logurile pentru a face debug-ul mai usor. Aceasta a fost implementata prin intermediul clasei
de logging.

Intregul enunt a fost implementat -UnitTesting. Programul trece toate testele.

Pentru realizarea temei m-am folosit de  laboratoarele 1, 2 si 3 de ASC


