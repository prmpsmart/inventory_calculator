import os

os.system("cls")


def money(value: int) -> str:
    return f"₦ {value:,.0f}"


def log(label: str, value: int):
    dash_length = 100 - len(label)
    dashes = "-" * dash_length
    print(f"{label} {dashes} {money(value)}")


def table(datas: list[tuple[str, int]]):
    for data in datas:
        label, value = data

        dash_length = 50 - len(label)
        dashes = "-" * dash_length

        print(f"\t{label} {dashes} {money(value)}")
    print()


months = 10
loan7 = 700_000
# loan7 = 0
mloan7 = loan7 / months
loan9 = 900_000
mloan9 = loan9 / months
loan16 = 1_600_000
mloan16 = loan16 / months

print()

loans = loan7 + loan9 + loan16
log(f"Total loans from Miracle", loans)
table(
    [
        ("Emergency loan (700k)", loan7),
        ("Cooperative loan", loan9),
        ("Cooperative loan", loan16),
    ]
)

rloan9 = 3
rloan16 = 2

repaid = (loan9 / months * rloan9) + (loan16 / months * rloan16)
log(f"Total repaid to Miracle", repaid)
table(
    [
        (
            f"{money(mloan9)} x {rloan9} = {money(mloan9 * rloan9)}    remaining",
            mloan9 * (months - rloan9),
        ),
        (
            f"{money(mloan16)} x {rloan16} = {money(mloan16 * rloan16)}    remaining",
            mloan16 * (months - rloan16),
        ),
    ]
)


loans -= repaid
log("Remaining loans from Miracle", loans)

print("\nOSCOFED Account:")
current_oscofed_savings = 600_000
log(f"Current OSCOFED savings", current_oscofed_savings)

current_oscofed_loan = 400_000
log(f"Current OSCOFED loan", current_oscofed_loan)

print()


def plan(id: int, target: int):
    print(f"Plan {id}")
    oscofed_saving_for_loan = target
    pump = oscofed_saving_for_loan - current_oscofed_savings + current_oscofed_loan

    log(
        f"1. Amount that Miracle will add to move OSCOFED savings to {money(oscofed_saving_for_loan)} for new loan",
        pump,
    )
    log(f"2. OSCOFED savings is now", oscofed_saving_for_loan)
    oscofed = oscofed_saving_for_loan * 2
    log(
        f"3. Loan to collect from OSCOFED ({money(oscofed_saving_for_loan)} x 2)",
        oscofed,
    )

    print()

    actual_loan_repay = oscofed - pump
    actual_loan_repay_text = f" ({money(oscofed)} - {money(pump)})"
    # if id == 2:
    #     actual_loan_repay = loan9
    #     actual_loan_repay = 1_000_000
    #     actual_loan_repay_text = ''
    log(
        f"4. Actual loan repaid to Miracle using the OSCOFED loan{actual_loan_repay_text}",
        actual_loan_repay,
    )

    remaining = loans - actual_loan_repay
    log(
        f"5. Loans from Miracle will remain ({money(loans)} - {money(actual_loan_repay)})",
        remaining,
    )

    mom_remaining_loan = oscofed + remaining
    log(
        f"6. Mom's remaining loan will now be",
        mom_remaining_loan,
    )
    table(
        [
            ("Miracle", remaining),
            ("OSCOFED", oscofed),
        ]
    )

    mom_repay_per_month = mom_remaining_loan / 10
    log(
        f"7. Mom's monthly loan repayment will now be {money(mom_remaining_loan)} / 10",
        mom_repay_per_month,
    )
    table(
        [
            ("Miracle", remaining / 10),
            ("OSCOFED", oscofed / 10),
        ]
    )


# plan(1, 1_000_000)
plan(2, 1_500_000)
