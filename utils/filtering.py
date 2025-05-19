from typing import List, Any

def get_extras_list(reservation: Any) -> List[str]:
    # TODO: Implement logic to get the list of extras from a reservation
    # return a list of strings, each representing an extra
    # reservation is a ResortReport object
    # return a list of strings, each representing an extra
    # reservation.extras_aggregated is a string form of "1x Extra - Child seat for Transfer - Airport to Resort (Bitez Tourism Extras), 1x Extra - Child seat for Transfer - Resort to Airport (Bitez Tourism Extras), 1x Extra - Welcome Pack  1-4 passengers (Resital Group Extras), 1x Extra - Damage Waiver (Solmar..."
    # the list of extras is the list of strings after "1x Extra -" mainly Pool Heating, Welcome Pack, Complementary Cot, etc.
    # but we dont want to include the number of extras and the word parantheses for company names like Bitez Tourism Extras, Resital Group Extras, etc.
    # so we want to return a list of strings like ["Pool Heating", "Welcome Pack", "Complementary Cot"]
    return [extra.split(" - ")[1].split(" (")[0] for extra in reservation.extras_aggregated.split(", ") if "1x Extra -" in extra]

def filter_reservations_by_villa_rules(reservations: List[Any], extras: List[str]) -> List[Any]:
    # TODO: Implement filtering logic based on villa assignments and rules
    # Document the expected shape of villa_assignments and rules
    # villa assignments is a dict of villa name to extras

    return reservations

def filter_passenger_infos_by_villa_rules(passenger_infos: List[Any], villa_assignments: Any, rules: Any) -> List[Any]:
    # TODO: Implement filtering logic for passenger infos
    # Document the expected shape of villa_assignments and rules
    return passenger_infos

def create_future_reservation_output(filtered_reservations: List[Any]) -> Any:
    # TODO: Format filtered reservations into the desired output structure
    return filtered_reservations

def create_future_apis_output(filtered_passenger_infos: List[Any]) -> Any:
    # TODO: Format filtered passenger infos into the desired API response
    return filtered_passenger_infos 

def filter_reservations_by_extras(reservations: List[Any], extras: List[str]) -> List[Any]:
    # TODO: Implement filtering logic for reservations by extras
    # reservations is a list of ResortReport objects
    # extras is a list of strings, each representing an extra
    # return a list of ResortReport objects

    # Filter reservations by extras
    filtered_reservations = []
    for reservation in reservations:
        if any([extra in get_extras_list(reservation) for extra in extras]):
            filtered_reservations.append(reservation)

    return filtered_reservations

def filter_reservations_by_extras_and_villa_rules(reservations: List[Any], extras: List[str], villa_assignments: Any, rules: Any) -> List[Any]:
    # TODO: Implement filtering logic for reservations by extras and villa rules
    return reservations